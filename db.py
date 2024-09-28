import pymysql.cursors

# Database connection details
host = 'localhost'
user = 'root'
password = ''
database = 'atm_data'

# Connect to MySQL server
connection = pymysql.connect(
    host=host,
    user=user,
    password=password
)

# Create a cursor object
cursor = connection.cursor()

# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

# Connect to the database
connection.select_db(database)

# Create sites_master table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        IP_Address VARCHAR(15) NOT NULL,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Port INT NOT NULL,
        Camera_1 VARCHAR(50),
        Camera_2 VARCHAR(50),
        Camera_3 VARCHAR(50),
        Camera_4 VARCHAR(50),
        DVR_name VARCHAR(50),
        Ping VARCHAR(10),
        Login_Status VARCHAR(10),
        HDD_Status VARCHAR(20),
        DVR_Time DATETIME
    )
""")

# Create dvr_status table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dvr_status (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip_address VARCHAR(15) NOT NULL,
        port_status VARCHAR(50),
        ping_status VARCHAR(50)
    )
""")

# Close the cursor and connection
cursor.close()
connection.close()

print("Database and tables created successfully.")
