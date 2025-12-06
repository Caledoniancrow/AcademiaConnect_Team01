import pyodbc
from flask import current_app, g

def get_db():

    if 'db' not in g:
        try:
            connection_string = current_app.config['SQL_CONN_STR']
            g.db = pyodbc.connect(connection_string)
            g.db.autocommit = True 
        except Exception as e:
            print(f"Database Connection Error: {e}")
            return None
    
    return g.db

def close_db(e=None):
    
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
   
    app.teardown_appcontext(close_db)
