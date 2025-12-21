import pyodbc
import subprocess

# First, make sure LocalDB is running
print("Starting LocalDB...")
try:
    subprocess.run(['sqllocaldb', 'start', 'MSSQLLocalDB'], 
                   capture_output=True, text=True, timeout=10)
    print("✓ LocalDB started\n")
except:
    print("Note: LocalDB might already be running\n")

# Test connection string
conn_str = (
    "Driver={SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=master;"  # Connect to master first to check if our DB exists
    "Trusted_Connection=yes;"
)

try:
    print("Connecting to SQL Server...")
    conn = pyodbc.connect(conn_str, timeout=10)
    print("✓ Connection successful!")
    
    cursor = conn.cursor()
    
    # Check SQL Server version
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"\nSQL Server Version:\n{row[0][:100]}...")
    
    # Check if our database exists
    cursor.execute("SELECT name FROM sys.databases WHERE name = 'AcademiaConnectDB'")
    db = cursor.fetchone()
    
    if db:
        print(f"\n✓ Database 'AcademiaConnectDB' already exists!")
    else:
        print("\nDatabase 'AcademiaConnectDB' does NOT exist.")
        print("Creating database...")
        cursor.execute("CREATE DATABASE AcademiaConnectDB")
        conn.commit()
        print("✓ Database created successfully!")
    
    conn.close()
    print("\n" + "="*50)
    print("Connection test PASSED!")
    print("You can now run your Flask application.")
    
except Exception as e:
    print(f"\n✗ Connection failed!")
    print(f"Error: {e}")
    print("\n" + "="*50)
    print("Troubleshooting:")
    print("1. Make sure LocalDB is started: sqllocaldb start MSSQLLocalDB")
    print("2. Check available drivers: python check_drivers.py")
    print("3. Try using ODBC Driver 17 instead of 'SQL Server'")