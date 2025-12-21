import subprocess
import time

print("Starting LocalDB instance...")
print("-" * 50)

try:
    # Start the LocalDB instance
    result = subprocess.run(['sqllocaldb', 'start', 'MSSQLLocalDB'], 
                          capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode == 0:
        print("✓ LocalDB started successfully!")
        
        # Get instance info
        time.sleep(2)
        info = subprocess.run(['sqllocaldb', 'info', 'MSSQLLocalDB'], 
                            capture_output=True, text=True)
        print("\nInstance Information:")
        print(info.stdout)
    else:
        print(f"Error: {result.stderr}")
        
except Exception as e:
    print(f"Error: {e}")