import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed'
    DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    USERS_CSV = os.path.join(DATA_DIR, 'users.csv')
    ISSUES_CSV = os.path.join(DATA_DIR, 'issues.csv')

    # Common Mercedes-Benz Car Models
    MERCEDES_CARLINES = [
        'A-Class', 'C-Class', 'E-Class', 'S-Class',
        'CLA', 'CLS', 'GLA', 'GLC', 'GLE', 'GLS',
        'AMG GT', 'G-Class', 'EQE', 'EQS', 'EQA', 'EQB'
    ]

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True) 