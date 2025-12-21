import pyodbc
import os

# --- 1. SETTINGS ---
SERVER = 'localhost'
DATABASE = 'AcademiaConnectDB'

# Connection string to connect to 'master' (to create the DB)
conn_str_master = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server={SERVER};"
    f"Database=master;"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
    f"Encrypt=yes;"
)

# SQL Commands to set up the database
setup_sql = [
    # 1. Create Database
    f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{DATABASE}') CREATE DATABASE [{DATABASE}]",
    
    # 2. Users Table
    f"""USE [{DATABASE}]; 
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
    CREATE TABLE dbo.Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        Username VARCHAR(50) UNIQUE NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        PasswordHash VARCHAR(255) NOT NULL,
        Role VARCHAR(20) CHECK (Role IN ('Industry', 'Student', 'Admin','Faculty'))
    );""",

    # 3. Projects Table
    f"""USE [{DATABASE}];
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Projects')
    CREATE TABLE dbo.Projects (
        ProjectID INT IDENTITY(1,1) PRIMARY KEY,
        Title VARCHAR(150) NOT NULL,
        Description NVARCHAR(MAX),
        Status VARCHAR(20) DEFAULT 'Open',
        IndustryID INT NULL FOREIGN KEY REFERENCES dbo.Users(UserID)
    );""",

    # 4. Teams Table
    f"""USE [{DATABASE}];
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Teams')
    CREATE TABLE dbo.Teams (
        TeamID INT IDENTITY(1,1) PRIMARY KEY,
        TeamName NVARCHAR(100) NOT NULL,
        LeaderID INT NOT NULL FOREIGN KEY REFERENCES dbo.Users(UserID),
        CreatedDate DATETIME DEFAULT GETDATE()
    );""",

    # 5. TeamMembers Table
    f"""USE [{DATABASE}];
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TeamMembers')
    CREATE TABLE dbo.TeamMembers (
        TeamID INT NOT NULL FOREIGN KEY REFERENCES dbo.Teams(TeamID),
        StudentID INT NOT NULL FOREIGN KEY REFERENCES dbo.Users(UserID),
        CONSTRAINT PK_TeamMembers PRIMARY KEY (TeamID, StudentID)
    );""",

    # 6. Applications Table
    f"""USE [{DATABASE}];
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Applications')
    CREATE TABLE dbo.Applications (
        ApplicationID INT IDENTITY(1,1) PRIMARY KEY,
        TeamID INT NOT NULL FOREIGN KEY REFERENCES dbo.Teams(TeamID),
        ProjectID INT NOT NULL FOREIGN KEY REFERENCES dbo.Projects(ProjectID),
        FacultyID INT NULL FOREIGN KEY REFERENCES dbo.Users(UserID),
        TeamStatement NVARCHAR(MAX),
        Status NVARCHAR(50) DEFAULT 'Pending Faculty',
        ApplicationDate DATETIME DEFAULT GETDATE()
    );""",

    # 7. Milestones Table
    f"""USE [{DATABASE}];
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Milestones')
    CREATE TABLE dbo.Milestones (
        MilestoneID INT IDENTITY(1,1) PRIMARY KEY,
        ProjectID INT NOT NULL FOREIGN KEY REFERENCES dbo.Projects(ProjectID),
        Title NVARCHAR(100) NOT NULL,
        Description NVARCHAR(MAX),
        Deadline DATETIME,
        Status NVARCHAR(50) DEFAULT 'Pending',
        SubmissionLink NVARCHAR(MAX) NULL,
        Grade INT NULL
    );"""
]

# Content for the new config.py file
config_file_content = f"""import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'team01-dev-key'
    
    # Database Settings
    SQL_SERVER = '{SERVER}'
    SQL_DATABASE = '{DATABASE}'
    
    # Connection String
    SQL_CONN_STR = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={{SQL_SERVER}};'
        f'DATABASE={{SQL_DATABASE}};'
        f'Trusted_Connection=yes;'
        f'TrustServerCertificate=yes;'
        f'Encrypt=yes;'
    )
"""

def fix_all():
    print("--- AUTOMATED FIX TOOL ---")
    
    # STEP 1: Fix Database
    print(f"1. Connecting to SQL Server ({SERVER})...")
    try:
        conn = pyodbc.connect(conn_str_master, autocommit=True)
        cursor = conn.cursor()
        print("   ✓ Connected.")
        
        print("2. Creating Database and Tables...")
        for query in setup_sql:
            cursor.execute(query)
        print("   ✓ Database Setup Complete.")
        conn.close()
    except Exception as e:
        print(f"   X ERROR Connecting to SQL: {e}")
        return

    # STEP 2: Fix config.py
    print("3. Writing new config.py file...")
    try:
        with open('config.py', 'w') as f:
            f.write(config_file_content)
        print("   ✓ config.py created successfully.")
    except Exception as e:
        print(f"   X Error writing file: {e}")
        return

    print("\n--- DONE! ---")
    print("You can now run: python run.py")

if __name__ == "__main__":
    fix_all()