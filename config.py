import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'scrt_key-@jbportal11'
    
    # Use PostgreSQL if available, otherwise fallback to SQLite
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///jobportal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
