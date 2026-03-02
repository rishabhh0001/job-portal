"""
Run this once to populate the database with dummy data for testing.
Usage: python seed_data.py
"""

from app import app
from extensions import db
from models import User, Job, Application
from werkzeug.security import generate_password_hash



def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Employers ──────────────────────────────────────────────
        google = User(
            username='google_recruiter',
            email='hire@google.com',
            password_hash=generate_password_hash('password123'),
            role='employer',
            company_name='Google'
        )
        stripe = User(
            username='stripe_hr',
            email='hire@stripe.com',
            password_hash=generate_password_hash('password123'),
            role='employer',
            company_name='Stripe'
        )
        swiggy = User(
            username='swiggy_talent',
            email='hire@swiggy.in',
            password_hash=generate_password_hash('password123'),
            role='employer',
            company_name='Swiggy'
        )

        # ── Admin ──────────────────────────────────────────────────
        admin = User(
            username='admin',
            email='admin@jobportal.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )

        # ── Seekers ────────────────────────────────────────────────
        ravi = User(
            username='ravi_sharma',
            email='ravi@example.com',
            password_hash=generate_password_hash('password123'),
            role='seeker'
        )
        priya = User(
            username='priya_nair',
            email='priya@example.com',
            password_hash=generate_password_hash('password123'),
            role='seeker'
        )

        db.session.add_all([google, stripe, swiggy, admin, ravi, priya])
        db.session.flush()  # get IDs before adding jobs

        # ── Engineering Jobs ───────────────────────────────────────
        j1 = Job(
            title='Senior Frontend Engineer',
            description='We are looking for a Senior Frontend Engineer to build and improve our consumer-facing products.\n\nYou will work closely with product designers and backend engineers to ship new features and improve existing ones. You should be comfortable working in a fast-paced environment and taking ownership of complex UI challenges.\n\nResponsibilities:\n- Build high-quality React components and features\n- Collaborate with designers on UX implementation\n- Improve core web vitals and frontend performance\n- Mentor junior engineers and review code',
            location='Bangalore / Remote',
            salary='₹35L - 55L PA',
            category='Engineering',
            job_type='Full Time',
            experience='4-7 years',
            skills='React, TypeScript, Next.js, GraphQL, CSS',
            employer_id=google.id
        )
        j2 = Job(
            title='Backend Engineer - Payments',
            description='Join Stripe\'s core payments team and help process billions of dollars in transactions every year.\n\nYou\'ll work on systems that need to be reliable, fast, and secure. Experience with distributed systems and high-throughput APIs is a must.\n\nResponsibilities:\n- Design and build payment processing infrastructure\n- Improve system reliability and reduce latency\n- Work on fraud detection and risk systems\n- Write thorough documentation and runbooks',
            location='Remote',
            salary='$180K - $240K',
            category='Engineering',
            job_type='Remote',
            experience='5-8 years',
            skills='Go, Ruby, Distributed Systems, PostgreSQL, Redis',
            employer_id=stripe.id
        )
        j3 = Job(
            title='Data Engineer',
            description='Swiggy is looking for a Data Engineer to build and maintain data pipelines that power our analytics and ML teams.\n\nYou will own end-to-end data workflows — from ingestion to serving — and work closely with analysts and data scientists.\n\nResponsibilities:\n- Build scalable ETL pipelines using Spark and Airflow\n- Maintain data warehouse on BigQuery\n- Implement data quality checks\n- Collaborate with ML team on feature engineering',
            location='Bangalore',
            salary='₹25L - 40L PA',
            category='Data Science',
            job_type='Full Time',
            experience='3-5 years',
            skills='Python, Apache Spark, Airflow, BigQuery, SQL',
            employer_id=swiggy.id
        )

        # ── Design Jobs ────────────────────────────────────────────
        j4 = Job(
            title='Product Designer',
            description='We\'re hiring a Product Designer who is passionate about creating intuitive, beautiful experiences for millions of users.\n\nYou\'ll own design end-to-end: from early ideation and user research to high-fidelity prototypes and final assets.\n\nResponsibilities:\n- Lead design for new product features\n- Conduct user research and usability testing\n- Maintain and evolve our design system\n- Partner closely with engineering during implementation',
            location='Hyderabad / Remote',
            salary='₹20L - 32L PA',
            category='Design',
            job_type='Full Time',
            experience='3-5 years',
            skills='Figma, User Research, Prototyping, Design Systems',
            employer_id=swiggy.id
        )
        j5 = Job(
            title='UX Researcher',
            description='Google is looking for a UX Researcher who can uncover insights that shape how hundreds of millions of people interact with our products.\n\nYou will design and execute research studies, synthesize findings, and work with cross-functional teams to drive product decisions.\n\nResponsibilities:\n- Plan and execute qualitative and quantitative research\n- Translate user insights into actionable recommendations\n- Present findings to product and leadership teams\n- Develop shared research tools and processes',
            location='Gurgaon',
            salary='₹28L - 45L PA',
            category='Design',
            job_type='Full Time',
            experience='3-6 years',
            skills='User Research, Surveys, Usability Testing, Data Analysis',
            employer_id=google.id
        )

        # ── Finance / Marketing ────────────────────────────────────
        j6 = Job(
            title='Growth Marketing Manager',
            description='Stripe is looking for a Growth Marketing Manager to drive user acquisition and engagement across our developer and SMB segments.\n\nYou\'ll run experiments, analyze performance, and work with the content and design teams to build campaigns that convert.\n\nResponsibilities:\n- Own paid and organic acquisition channels\n- Run A/B experiments on landing pages and ad creatives\n- Analyze cohort data and optimize CAC/LTV\n- Work with sales on pipeline generation',
            location='Remote',
            salary='$120K - $160K',
            category='Marketing',
            job_type='Remote',
            experience='4-6 years',
            skills='Growth Marketing, SQL, Google Ads, Analytics, A/B Testing',
            employer_id=stripe.id
        )

        db.session.add_all([j1, j2, j3, j4, j5, j6])
        db.session.flush()

        # ── Sample Applications ────────────────────────────────────
        db.session.add_all([
            Application(job_id=j1.id, seeker_id=ravi.id, status='Reviewing'),
            Application(job_id=j3.id, seeker_id=ravi.id, status='Applied'),
            Application(job_id=j2.id, seeker_id=priya.id, status='Applied'),
            Application(job_id=j4.id, seeker_id=priya.id, status='Accepted'),
        ])

        db.session.commit()
        print("[OK] Database seeded successfully")
        print(f"  -> {len([google, stripe, swiggy, admin, ravi, priya])} users created")
        print(f"  -> {len([j1, j2, j3, j4, j5, j6])} jobs created across 3 companies")
        print(f"  -> 4 test applications added")
        print()
        print("Test accounts:")
        print("  Seeker  -> ravi@example.com / password123")
        print("  Seeker  -> priya@example.com / password123")
        print("  Employer -> hire@google.com / password123  (Google)")
        print("  Employer -> hire@stripe.com / password123  (Stripe)")
        print("  Employer -> hire@swiggy.in / password123   (Swiggy)")
        print("  Admin   -> admin@jobportal.com / admin123")


if __name__ == '__main__':
    seed()
