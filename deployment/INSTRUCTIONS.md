# Deployment Guide for Academia Connect

## Prerequisites
1. Python 3.9+ installed.
2. Microsoft SQL Server (Express or LocalDB) installed.
3. ODBC Driver 17 for SQL Server installed.

## Step 1: Database Setup
1. Open SQL Server Management Studio (SSMS).
2. Create a new database named `AcademiaConnectDB`.
3. Open the file `deployment/database_schema.sql` in SSMS.
4. Execute the script to create the tables.

## Step 2: Application Setup
1. Navigate to the root folder.
2. Double-click `deployment/setup_env.bat` (or run `pip install -r requirements.txt`).
3. Create a `config.py` file in the root folder (see `config_template.py` for reference).
4. Update `config.py` with your Server Name.

## Step 3: Running
Run the following command in terminal:
`python run.py`