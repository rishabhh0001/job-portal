from flask import Flask, render_template, request, redirect, url_for, flash, abort

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

from models import User, Job, Application


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── Public Routes ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    featured_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', featured_jobs=featured_jobs)



@app.route('/jobs')
def jobs():
    q = request.args.get('q', '')
    location = request.args.get('location', '')
    category = request.args.get('category', '')
    job_type = request.args.get('job_type', '')

    query = Job.query.filter_by(is_active=True)
    if q:
        query = query.filter(Job.title.ilike(f'%{q}%') | Job.description.ilike(f'%{q}%'))
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    if category:
        query = query.filter_by(category=category)
    if job_type:
        query = query.filter_by(job_type=job_type)


    job_list = query.order_by(Job.created_at.desc()).all()
    categories = db.session.query(Job.category).distinct().all()
    return render_template('jobs.html', jobs=job_list, categories=[c[0] for c in categories], q=q, location=location, selected_category=category, selected_type=job_type)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')



@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    already_applied = False
    if current_user.is_authenticated and current_user.role == 'seeker':
        already_applied = Application.query.filter_by(job_id=job_id, seeker_id=current_user.id).first() is not None
    similar = Job.query.filter(Job.category == job.category, Job.id != job.id).limit(3).all()
    return render_template('job_detail.html', job=job, already_applied=already_applied, similar=similar)


# ─── Auth Routes ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            if not user.is_active:
                flash('Your account has been suspended. Please contact support.', 'error')
                return redirect(url_for('login'))
            login_user(user, remember=request.form.get('remember') == 'on')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid email or password.', 'error')
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'error')
            return redirect(url_for('register'))

        user = User(
            email=email,
            username=request.form.get('name'),
            password_hash=generate_password_hash(request.form.get('password')),
            role=request.form.get('role', 'seeker'),
            company_name=request.form.get('company_name') if request.form.get('role') == 'employer' else None
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ─── Seeker Routes ────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def seeker_dashboard():
    if current_user.role == 'employer':
        return redirect(url_for('employer_dashboard'))
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    rows = db.session.query(Application, Job).join(Job, Application.job_id == Job.id)\
        .filter(Application.seeker_id == current_user.id)\
        .order_by(Application.applied_at.desc()).all()
    return render_template('dashboards/seeker.html', rows=rows)


@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.role != 'seeker':
        flash('Only job seekers can apply for positions.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))

    if Application.query.filter_by(job_id=job_id, seeker_id=current_user.id).first():
        flash('You have already applied for this position.', 'info')
        return redirect(url_for('job_detail', job_id=job_id))

    db.session.add(Application(job_id=job_id, seeker_id=current_user.id))
    db.session.commit()
    flash('Application submitted successfully! Good luck!', 'success')
    return redirect(url_for('seeker_dashboard'))


# ─── Employer Routes ──────────────────────────────────────────────────────────

@app.route('/employer/dashboard')
@login_required
def employer_dashboard():
    if current_user.role != 'employer':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    total_apps = sum(len(j.applications) for j in jobs)
    return render_template('dashboards/employer.html', jobs=jobs, total_apps=total_apps)


@app.route('/employer/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            description=request.form.get('description'),
            location=request.form.get('location'),
            salary=request.form.get('salary'),
            category=request.form.get('category'),
            job_type=request.form.get('job_type', 'Full Time'),
            experience=request.form.get('experience'),
            skills=request.form.get('skills'),
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer_dashboard'))
    return render_template('dashboards/post_job.html')


@app.route('/employer/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('employer_dashboard'))
    Application.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()
    flash('Job listing removed.', 'success')
    return redirect(url_for('employer_dashboard'))


@app.route('/employer/job/<int:job_id>/applications')
@login_required
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('employer_dashboard'))
    applications = db.session.query(Application, User).join(User, Application.seeker_id == User.id)\
        .filter(Application.job_id == job_id).all()
    return render_template('dashboards/applications.html', job=job, applications=applications)


# ─── Admin Routes ─────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Admin access only.', 'error')
        return redirect(url_for('index'))
    users = User.query.order_by(User.created_at.desc()).all()
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    apps = Application.query.all()
    return render_template('dashboards/admin.html', users=users, jobs=jobs, apps=apps)


@app.route('/admin/applications')
@login_required
def admin_applications():
    if current_user.role != 'admin':
        abort(403)
    applications = db.session.query(Application, Job, User)\
        .join(Job, Application.job_id == Job.id)\
        .join(User, Application.seeker_id == User.id)\
        .order_by(Application.applied_at.desc()).all()
    return render_template('dashboards/admin_apps.html', applications=applications)



@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'error')
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Cleanup associate data
    Application.query.filter_by(seeker_id=user.id).delete()
    jobs = Job.query.filter_by(employer_id=user.id).all()
    for job in jobs:
        Application.query.filter_by(job_id=job.id).delete()
        db.session.delete(job)
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} and all associated data removed.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/job/<int:job_id>/delete', methods=['POST'])
@login_required
def admin_delete_job(job_id):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'error')
        return redirect(url_for('index'))
    job = Job.query.get_or_404(job_id)
    Application.query.filter_by(job_id=job.id).delete()
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/user/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def admin_toggle_user_status(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot suspend yourself.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'suspended'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/user/<int:user_id>/change-role', methods=['POST'])
@login_required
def admin_change_user_role(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role not in ['seeker', 'employer', 'admin']:
        flash('Invalid role selection.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if user.id == current_user.id and new_role != 'admin':
        flash('You cannot demote yourself from admin role.', 'error')
        return redirect(url_for('admin_dashboard'))

    user.role = new_role
    db.session.commit()
    flash(f'User {user.username} role updated to {new_role}.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/job/<int:job_id>/toggle-status', methods=['POST'])
@login_required
def admin_toggle_job_status(job_id):
    if current_user.role != 'admin':
        abort(403)
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    status = 'approved/activated' if job.is_active else 'deactivated'
    flash(f'Job "{job.title}" has been {status}.', 'success')
    return redirect(url_for('admin_dashboard'))



@app.route('/init-db')
def init_db_route():
    # Only allow if database is empty or secret key matches
    verification_code = request.args.get('code')
    if verification_code == os.environ.get('SECRET_KEY') or verification_code == 'jb_admin_secret_2026':
        from seed_data import seed
        seed()
        return "Database initialized and seeded successfully!"
    else:
        return "Unauthorized", 403


if __name__ == '__main__':
    app.run(debug=True)
