import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'scrt_key-@jbportal11'
    # Use PostgreSQL if available, otherwise fallback to SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jobportal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
