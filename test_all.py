import pyodbc
import subprocess

# Start LocalDB first
print("=" * 60)
print("STARTING LOCALDB")
print("=" * 60)
try:
    result = subprocess.run(['sqllocaldb', 'start', 'MSSQLLocalDB'], 
                          capture_output=True, text=True, timeout=10)
    print(result.stdout)
except Exception as e:
    print(f"LocalDB start error (might already be running): {e}")

print("\n" + "=" * 60)
print("CHECKING AVAILABLE DRIVERS")
print("=" * 60)
drivers = pyodbc.drivers()
for driver in drivers:
    print(f"  ✓ {driver}")

print("\n" + "=" * 60)
print("TESTING CONNECTION STRINGS")
print("=" * 60)

# Connection strings to test
test_configs = [
    {
        "name": "SQL Server with LocalDB",
        "conn_str": (
            "Driver={SQL Server};"
            "Server=(localdb)\\MSSQLLocalDB;"
            "Database=master;"
            "Trusted_Connection=yes;"
        )
    },
    {
        "name": "ODBC Driver 17 with LocalDB",
        "conn_str": (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=(localdb)\\MSSQLLocalDB;"
            "Database=master;"
            "Trusted_Connection=yes;"
        )
    },
    {
        "name": "SQL Server Native Client with LocalDB",
        "conn_str": (
            "Driver={SQL Server Native Client 11.0};"
            "Server=(localdb)\\MSSQLLocalDB;"
            "Database=master;"
            "Trusted_Connection=yes;"
        )
    },
]

working_config = None

for config in test_configs:
    print(f"\nTesting: {config['name']}")
    print("-" * 50)
    try:
        conn = pyodbc.connect(config['conn_str'], timeout=10)
        print("✓✓✓ SUCCESS! This configuration works! ✓✓✓")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Connected to: {version[:80]}...")
        
        working_config = config
        conn.close()
        break
        
    except Exception as e:
        print(f"✗ Failed: {str(e)[:100]}")

if working_config:
    print("\n" + "=" * 60)
    print("✓ WORKING CONFIGURATION FOUND!")
    print("=" * 60)
    print("\nAdd this to your config.py:")
    print("-" * 50)
    print(f"SQL_CONN_STR = (")
    for line in working_config['conn_str'].split(';'):
        if line.strip():
            print(f'{line}')
else:
    print("\n" + "=" * 60)
    print("✗ NO WORKING CONFIGURATION FOUND")
    print("=" * 60)
    print("\nTroubleshooting steps:")
    print("1. Install ODBC Driver 17: https://go.microsoft.com/fwlink/?linkid=2249004")
    print("2. Run as Administrator: sqllocaldb start MSSQLLocalDB")
    print("3. Check Windows Services: SQL Server (MSSQLSERVER) is running")