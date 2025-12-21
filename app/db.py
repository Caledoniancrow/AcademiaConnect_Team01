import pyodbc
from flask import current_app, g

def get_db():
    """Get database connection from Flask's g object"""
    if 'db' not in g:
        try:
            connection_string = current_app.config.get('SQL_CONN_STR')
            
            if not connection_string:
                print("[ERROR] SQL_CONN_STR not found in config")
                return None
            
            print(f"[DEBUG] Attempting connection with: {connection_string}")
            g.db = pyodbc.connect(connection_string)
            g.db.autocommit = False  # Change to False for manual commit control
            print("[SUCCESS] Database connected")
            
        except pyodbc.Error as e:
            print(f"[ERROR] Database Connection Error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return None
    
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    
    if db is not None:
        try:
            db.close()
            print("[DEBUG] Database connection closed")
        except Exception as ex:
            print(f"[ERROR] Error closing database: {ex}")

def init_app(app):
    """Initialize database with Flask app"""
    app.teardown_appcontext(close_db)