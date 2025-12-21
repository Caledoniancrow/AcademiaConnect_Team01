import os

class Config:
    # 1. SECRET_KEY: Used for session security (login cookies)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'team01-dev-key'
    
    # 2. DATABASE CONFIGURATION
    # INSTRUCTIONS: 
    # Replace 'YOUR_SERVER_NAME' with your specific SQL Server instance.
    # Example: 'DESKTOP-558\SQLEXPRESS' or 'localhost'
    SQL_SERVER = 'localhost' 
    SQL_DATABASE = 'AcademiaConnectDB'
    #localhost
    
    # 3. CONNECTION STRING
    # 'Trusted_Connection=yes' means it uses your Windows Login (No password needed)
    SQL_CONN_STR = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SQL_SERVER};'
        f'DATABASE={SQL_DATABASE};'
        f'Trusted_Connection=yes;'
    )