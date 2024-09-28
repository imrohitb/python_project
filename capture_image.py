import cv2
import mysql.connector
import hashlib

# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()

# Create the atm_data database
cursor.execute("CREATE DATABASE IF NOT EXISTS atm_data")

# Use the created database
cursor.execute("USE atm_data")

# Create the atm_data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS atm_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ATM VARCHAR(255) NOT NULL,
    IP_ADDRESS VARCHAR(255) NOT NULL,
    RTSP_URL VARCHAR(255) NOT NULL
)
""")

# Commit the changes
connection.commit()

# Insert sample data
sample_data = [
    ("ATM-001", "192.168.1.1", "rtsp://192.168.1.1/stream"),
    ("ATM-002", "192.168.1.2", "rtsp://192.168.1.2/stream"),
    # Add more entries as needed
]

for atm_id, ip_address, rtsp_url in sample_data:
    cursor.execute("INSERT INTO atm_data (ATM, IP_ADDRESS, RTSP_URL) VALUES (%s, %s, %s)", (atm_id, ip_address, rtsp_url))

# Commit the changes
connection.commit()

# Fetch the ATM, IP address, and RTSP URL from the database
cursor.execute("SELECT ATM, IP_ADDRESS, RTSP_URL FROM atm_data")
results = cursor.fetchall()

# Iterate through the results
for row in results:
    atm_id, ip_address, rtsp_url = row

    # Generate a filename using the ATM ID and current timestamp
    filename = f"{atm_id}_{int(time.time())}.jpg"

    # Open the RTSP stream and capture a frame
    cap = cv2.VideoCapture(rtsp_url)
    ret, frame = cap.read()

    if ret:
        # Save the frame as an image file
        cv2.imwrite(filename, frame)
        print(f"Image saved: {filename}")

        # Close the capture
        cap.release()

    else:
        print(f"Failed to capture image from RTSP URL: {rtsp_url}")

# Close the cursor and connection
cursor.close()
connection.close()