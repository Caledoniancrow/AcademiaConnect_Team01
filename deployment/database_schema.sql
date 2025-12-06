CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Role VARCHAR(20) CHECK (Role IN ('Industry', 'Student', 'Admin'))
);


CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY IDENTITY(1,1),
    Title VARCHAR(150) NOT NULL,
    Description TEXT,
    Status VARCHAR(20) DEFAULT 'Open',
    IndustryID INT FOREIGN KEY REFERENCES Users(UserID)
);