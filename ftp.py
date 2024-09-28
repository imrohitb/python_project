import cv2
from ftplib import FTP
import numpy as np
import time

# RTSP stream URL
rtsp_url = "rtsp://admin:css@12345@10.109.8.131:554/unicast/c1/s1/live"

# FTP server settings
ftp_server = "ftp://192.168.100.26:7554"
ftp_username = "comfort"
ftp_password = "cam@12345"
ftp_directory = "AI_FTP"

# Create an FTP connection
ftp = FTP(ftp_server)
ftp.login(user=ftp_username, passwd=ftp_password)

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from RTSP stream.")
        break

    # Convert the frame to bytes
    frame_bytes = cv2.imencode(".jpg", frame)[1].tobytes()

    # Upload the frame to the FTP server
    timestamp = time.strftime("%Y%m%d%H%M%S")
    remote_filename = f"frame_{timestamp}.jpg"
    try:
        ftp.storbinary(f"STOR {ftp_directory}/{remote_filename}", frame_bytes)
        print(f"Uploaded frame: {remote_filename}")
    except Exception as e:
        print(f"Error uploading frame: {e}")

    # Delay to control the frame capture rate (adjust as needed)
    time.sleep(1)

# Release resources
cap.release()
cv2.destroyAllWindows()
ftp.quit()
