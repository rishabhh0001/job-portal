from extensions import db
from flask_login import UserMixin
from datetime import datetime



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='seeker')  # seeker / employer / admin
    company_name = db.Column(db.String(100))  # only for employers
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    jobs = db.relationship('Job', backref='employer', lazy=True, foreign_keys='Job.employer_id')
    applications = db.relationship('Application', backref='seeker', lazy=True, foreign_keys='Application.seeker_id')


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(60))
    category = db.Column(db.String(60))
    job_type = db.Column(db.String(40), default='Full Time')  # Full Time / Part Time / Contract / Remote
    experience = db.Column(db.String(40))  # e.g. 2-4 years
    skills = db.Column(db.String(200))  # comma separated
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    applications = db.relationship('Application', backref='job', lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied')  # Applied / Reviewing / Accepted / Rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
