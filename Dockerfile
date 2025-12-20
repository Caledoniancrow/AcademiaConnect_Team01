# Use Debian 11 (Bullseye) which is 100% compatible with MS SQL Drivers
FROM python:3.9-slim-bullseye

# 1. Install ESSENTIAL system tools first (curl, gnupg2) so commands exist
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 2. Add the Microsoft Key and Repository (Specific to Debian 11)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# 3. Install the SQL Server Driver
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# 4. Set Work Directory
WORKDIR /app

# 5. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy App Code
COPY . .

# 7. Expose Port
EXPOSE 5000

# 8. Run App
CMD ["python", "run.py"]