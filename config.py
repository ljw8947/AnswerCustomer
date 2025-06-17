import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed'
    DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    USERS_CSV = os.path.join(DATA_DIR, 'users.csv')
    ISSUES_CSV = os.path.join(DATA_DIR, 'issues.csv')
    COMMENTS_CSV = os.path.join(DATA_DIR, 'comments.csv')
    CATEGORY_CSV = os.path.join(DATA_DIR, 'category.csv')

    # Common Mercedes-Benz Car Models
    MERCEDES_CARLINES = [
        'A-Class', 'C-Class', 'E-Class', 'S-Class',
        'CLA', 'CLS', 'GLA', 'GLC', 'GLE', 'GLS',
        'AMG GT', 'G-Class', 'EQE', 'EQS', 'EQA', 'EQB',
        '177', '118', '213', '247', '293', '206', '294', '223', '214', '254', '243', '167', '295', '297', '253'
    ]

    # Power Types
    POWER_TYPES = ['ICE', 'BEV', 'PHEV', 'Unknown']

    # Specific Functions
    SPECIFIC_FUNCTIONS = [
        'Driving Assist', 'Remote Control', 'Smart Phone Integration', 'Active safety',
        'UIUX', 'Digital Key', 'APP Performance', 'Mme Profile', 'In-car Navigation',
        'Connectivity/OTA', 'Battery/Charging', 'In/exterior', 'Braking System',
        'NVH', 'Seat', 'Drivetrain', 'Headlights', 'Cabin Light', 'Chassis'
    ]

    # Function Domains
    FUNCTION_DOMAINS = [
        'ADAS', 'Mme APP', 'Smart Cabin', 'Drivetrain', 'Overall Vehicle'
    ]

    # General Domains
    GENERAL_DOMAINS = ['Software', 'Hardware']

    # Issue Types
    ISSUE_TYPES = [
        'User Experience Issue', 'New Requirement', 'Malfunction', 'Inquiry'
    ]

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True) 