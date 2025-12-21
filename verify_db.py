import pyodbc
from config import Config

print("--- DIAGNOSTIC TOOL ---")
print(f"Target Database: {Config.SQL_DATABASE}")

try:
    # 1. Try to Connect
    conn = pyodbc.connect(Config.SQL_CONN_STR)
    cursor = conn.cursor()
    print("✓ Connection Successful!")

    # 2. Check for Users Table
    try:
        cursor.execute("SELECT COUNT(*) FROM Users")
        count = cursor.fetchone()[0]
        print(f"✓ Table 'Users' found! (Contains {count} users)")
    except Exception as e:
        print("X ERROR: Table 'Users' not found.")
        print("  Hint: You connected to the DB, but it's empty.")
        print("  Fix: Run the SQL script in Step 2 above.")

except Exception as e:
    print("X Connection Failed.")
    print(f"  Error: {e}")
    print("  Fix: Check your config.py connection string.")