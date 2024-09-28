import cv2
import os
import pymysql.cursors
import time


# Function to capture snapshot with timeout and error handling
def capture_snapshot(atm_info):
    atm_id, username, password, ip_address, dvr_name = atm_info
    try:
        # Construct RTSP URL based on DVR Name
        if dvr_name.lower() == 'hikvision':
            rtsp_url = f"rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/101"
        elif dvr_name.lower() == 'cpplus':
            rtsp_url = f"rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0"
        elif dvr_name.lower() == 'unv':
            rtsp_url = f"rtsp://{username}:{password}@{ip_address}:554/unicast/c1/s1/live"
        else:
            rtsp_url = f"rtsp://{username}:{password}@{ip_address}/stream"

        print(f"Processing ATM ID {atm_id}: {rtsp_url}")

        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print(f"Error: Unable to open RTSP connection for ATM ID {atm_id}")
            return atm_id, "failed"

        start_time = time.time(5)
        while True:
            ret, frame = cap.read()
            if ret:
                # Save the snapshot with ATM ID as filename
                folder_path = "D:/Rohit/snapshot"
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, f"{atm_id}.jpg")
                cv2.imwrite(file_path, frame)
                print(f"Snapshot captured and saved for ATM ID {atm_id} at {file_path}")
                return atm_id, "successful"
            elif time.time() - start_time > 3:  # Increase timeout to 10 seconds
                print(f"Error: Timeout reached while capturing snapshot for ATM ID {atm_id}")
                return atm_id, "failed"
    except Exception as e:
        print(f"Error occurred while capturing snapshot for ATM ID {atm_id}: {str(e)}")
        return atm_id, "failed"


# Database connection parameters
host = "localhost"  # Hostname
user = "root"  # Username
password = ""  # Password, leave empty if no password
database = "atm_data"  # Database name

# Connect to the database
try:
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database,
                                 cursorclass=pymysql.cursors.DictCursor)

    # Fetch data from the database
    with connection.cursor() as cursor:
        sql = "SELECT ATM, `User Name`, `Password`, IP_Address, `DVR Name` FROM atm_info"
        cursor.execute(sql)
        results = cursor.fetchall()

        # Process ATM info one by one
        statuses = []
        for row in results:
            atm_info = (row['ATM'], row['User Name'], row['Password'], row['IP_Address'], row['DVR Name'])
            atm_id, status = capture_snapshot(atm_info)
            statuses.append((atm_id, status))

        # Insert snapshot reports into database
        try:
            with connection.cursor() as insert_cursor:
                for atm_id, status in statuses:
                    sql_insert = "INSERTINTO snapshot_reports (ATM_id, Status) VALUES (%s, %s)"
                    insert_cursor.execute(sql_insert, (atm_id, status))
            connection.commit()
        except Exception as e:
            print(f"Error occurred while inserting snapshot reports into database: {str(e)}")

finally:
    # Close the connection
    if 'connection' in locals():
        connection.close()