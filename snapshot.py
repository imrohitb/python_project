import cv2
import os
import time

def capture_snapshots(rtsp_urls_file, destination_folder):
    # Create destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Read RTSP URLs from file
    with open(rtsp_urls_file, "r") as file:
        rtsp_urls = file.readlines()

    # Remove whitespace characters from the beginning and end of each URL
    rtsp_urls = [url.strip() for url in rtsp_urls]

    # Capture one snapshot from each URL
    for i, rtsp_url in enumerate(rtsp_urls):
        # Open RTSP stream
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera opened successfully
        if not cap.isOpened():
            print(f"Error: Could not open RTSP stream {i + 1}.")
            continue

        # Capture one snapshot
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame from RTSP stream {i + 1}.")
            continue

        # Save the snapshot
        snapshot_path = os.path.join(destination_folder, f"snapshot_{i + 1}.jpg")
        cv2.imwrite(snapshot_path, frame)
        print(f"Snapshot from camera {i + 1} captured and saved.")

        # Release the capture
        cap.release()

        # Wait for 5 seconds before moving to the next URL
        time.sleep(2)

if __name__ == "__main__":
    rtsp_urls_file = "rtsp_urls.txt"  # Path to the file containing RTSP URLs
    destination_folder = "snapshots"  # Destination folder for saving snapshots

    capture_snapshots(rtsp_urls_file, destination_folder)
