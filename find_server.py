import subprocess

print("Looking for SQL Server instances...")
print("-" * 50)

try:
    # Method 1: Using sqllocaldb
    result = subprocess.run(['sqllocaldb', 'info'], capture_output=True, text=True)
    if result.returncode == 0:
        print("LocalDB Instances found:")
        print(result.stdout)
    
    # Method 2: Using sqlcmd
    result2 = subprocess.run(['sqlcmd', '-L'], capture_output=True, text=True, timeout=10)
    if result2.returncode == 0:
        print("\nSQL Server instances on network:")
        print(result2.stdout)
        
except FileNotFoundError:
    print("SQL Server tools not found in PATH")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Common server names to try:")
print("- (localdb)\\MSSQLLocalDB")
print("- localhost\\SQLEXPRESS")
print("- .\\SQLEXPRESS")
print("- localhost")
print("- YOUR_COMPUTER_NAME\\SQLEXPRESS")