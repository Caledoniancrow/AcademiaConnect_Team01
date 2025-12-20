IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        Username VARCHAR(50) UNIQUE NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        PasswordHash VARCHAR(255) NOT NULL,
        Role VARCHAR(20) CHECK (Role IN ('Industry', 'Student', 'Admin'))
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Projects' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.Projects (
        ProjectID INT IDENTITY(1,1) PRIMARY KEY,
        Title VARCHAR(150) NOT NULL,
        Description NVARCHAR(MAX),
        Status VARCHAR(20) DEFAULT 'Open',
        IndustryID INT NULL,
        CONSTRAINT FK_Projects_Users
            FOREIGN KEY (IndustryID) REFERENCES dbo.Users(UserID)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Teams' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.Teams (
        TeamID INT IDENTITY(1,1) PRIMARY KEY,
        TeamName NVARCHAR(100) NOT NULL,
        LeaderID INT NOT NULL,
        CreatedDate DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Teams_Users
            FOREIGN KEY (LeaderID) REFERENCES dbo.Users(UserID)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TeamMembers' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.TeamMembers (
        TeamID INT NOT NULL,
        StudentID INT NOT NULL,
        CONSTRAINT PK_TeamMembers PRIMARY KEY (TeamID, StudentID),
        CONSTRAINT FK_TeamMembers_Teams
            FOREIGN KEY (TeamID) REFERENCES dbo.Teams(TeamID),
        CONSTRAINT FK_TeamMembers_Users
            FOREIGN KEY (StudentID) REFERENCES dbo.Users(UserID)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Applications' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.Applications (
        ApplicationID INT IDENTITY(1,1) PRIMARY KEY,
        TeamID INT NOT NULL,
        ProjectID INT NOT NULL,
        TeamStatement NVARCHAR(MAX),
        Status NVARCHAR(50) DEFAULT 'Pending Faculty',
        ApplicationDate DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Applications_Teams
            FOREIGN KEY (TeamID) REFERENCES dbo.Teams(TeamID),
        CONSTRAINT FK_Applications_Projects
            FOREIGN KEY (ProjectID) REFERENCES dbo.Projects(ProjectID)
    );
END
GO