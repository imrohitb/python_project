import cv2
import os
import pandas as pd
from tqdm import tqdm
import time

def capture_video(rtsp_url, output_folder):
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise ValueError("RTSP stream not opened")

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_file = os.path.join(output_folder, 'output.avi')
        out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))

        # Capture video for 60 seconds
        start_time = time.time()
        while time.time() - start_time < 60:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_rtsp_urls(file_path, output_folder):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            rtsp_url = line.strip()
            if rtsp_url:
                success = False
                retry_count = 0
                while not success and retry_count < 3:
                    success = capture_video(rtsp_url, output_folder)
                    if not success:
                        retry_count += 1
                        print(f"Retrying for {rtsp_url}... Attempt {retry_count}")
                        time.sleep(5)  # Wait for 5 seconds before retrying
                if success:
                    results.append((rtsp_url, 'Download Successful'))
                else:
                    results.append((rtsp_url, 'Download Failed'))

    # Export results to Excel
    df = pd.DataFrame(results, columns=['RTSP URL', 'Status'])
    excel_file = os.path.join(output_folder, 'results.xlsx')
    df.to_excel(excel_file, index=False)
    print("\nResults exported to:", excel_file)

if __name__ == "__main__":
    rtsp_urls_file = "rtsp_urls.txt"  # Path to the file containing RTSP URLs
    video_output_folder = "videos"     # Output folder to store captured videos
    if not os.path.exists(video_output_folder):
        os.makedirs(video_output_folder)
    process_rtsp_urls(rtsp_urls_file, video_output_folder)
