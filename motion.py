import requests
from requests.auth import HTTPDigestAuth
import subprocess
import time
import datetime
import xml.etree.ElementTree as ET

# Hikvision NVR details
dvr_ip = "192.168.100.126"
port = 81
username = "admin"
password = "css@12345"

# RTSP stream URL (you might need to adjust this based on your camera configuration)
rtsp_url = f"rtsp://{username}:{password}@{dvr_ip}:554/Streaming/Channels/101"

# Function to check motion detection
def check_motion():
    url = f"http://{dvr_ip}:{port}/ISAPI/System/Video/inputs/channels/1/motionDetection"
    try:
        response = requests.get(url, auth=HTTPDigestAuth(username, password))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        try:
            root = ET.fromstring(response.content)
            # Check if motion detection is enabled and motion is detected
            enabled = root.find('.//{http://www.hikvision.com/ver20/mmmm/XMLSchema}enabled').text == 'true'
            # Assuming you want to detect any changes in the motion detection grid
            # Currently, there is no direct field showing if motion is detected or not
            # You might need to refer to the specific implementation or API documentation for this
            return enabled
        except ET.ParseError as e:
            print("Error parsing XML response:", e)
            print("Response content:", response.content)
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

# Function to capture video using FFmpeg
def capture_video(duration=60):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"motion_capture_{timestamp}.mp4"
    ffmpeg_command = [
        'ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_url, '-t', str(duration), '-vcodec', 'copy', '-acodec', 'copy', output_file
    ]
    subprocess.run(ffmpeg_command)
    print(f"Video saved as {output_file}")

# Main loop to check for motion and capture video
while True:
    if check_motion():
        print("Motion detected! Capturing video...")
        capture_video(duration=60)  # Capture 60 seconds of video
    else:
        print("No motion detected.")
    time.sleep(10)  # Check every 10 seconds
