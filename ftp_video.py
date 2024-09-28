import cv2
import time
import os
from ftplib import FTP

# FTP details
FTP_HOST = "192.168.100.26"
FTP_PORT = 7554
FTP_USER = "comfort"
FTP_PASS = "cam@12345"

# RTSP stream URL (Replace with your RTSP URL)
rtsp_url = "rtsp://admin:css12345@172.55.23.94:554/cam/realmonitor?channel=1&subtype=0"

# Function to upload file to FTP server
def upload_to_ftp(file_path, filename):
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)

        with open(file_path, 'rb') as file:
            ftp.storbinary(f"STOR {filename}", file)
        
        ftp.quit()
        print(f"Uploaded: {filename}")
    except Exception as e:
        print(f"Failed to upload {filename}. Error: {e}")

# Capture the RTSP stream and save frames to a video file
def capture_stream():
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Cannot open stream")
        return

    # Get the actual frame rate of the stream
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    if actual_fps == 0:
        actual_fps = 25.0  # Fallback to a default value if FPS can't be detected
    print(f"Detected frame rate: {actual_fps} FPS")

    while True:
        # Filename for the new video file (every 1 minute)
        filename = time.strftime("%Y%m%d_%H%M%S") + ".mp4"
        file_path = os.path.join("videos", filename)

        # Capture the first frame to determine frame size
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        height, width, _ = frame.shape
        print(f"Frame size: {width}x{height}")

        # Define the codec and create VideoWriter object with the detected FPS
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
        out = cv2.VideoWriter(file_path, fourcc, actual_fps, (width, height))

        start_time = time.time()

        # Record for 60 seconds (1 minute)
        while time.time() - start_time < 60:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Write the frame to the video file
            out.write(frame)

            # Optionally show the frame for debugging
            cv2.imshow('RTSP Stream', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video writer after the minute recording
        out.release()

        # Close the video display window
        cv2.destroyAllWindows()

        # Upload the saved video to FTP
        upload_to_ftp(file_path, filename)

        # Wait for a short moment to avoid processing too quickly
        time.sleep(1)

    # Release the video capture when done
    cap.release()

# Ensure the videos folder exists
os.makedirs("videos", exist_ok=True)

# Start capturing and uploading the stream
capture_stream()
