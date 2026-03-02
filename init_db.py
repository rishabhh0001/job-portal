from app import app, db
from models import User, Job, Application

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized and tables created.")

if __name__ == '__main__':
    init_db()
