import cv2
import numpy as np
import sqlite3
from datetime import datetime

# Initialize the database
conn = sqlite3.connect('snapshot_database.db')
cursor = conn.cursor()

# Create a table to store URLs and image file paths
cursor.execute('''
    CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        image_path TEXT
    )
''')
conn.commit()

def save_snapshot(url, frame):
    # Generate a unique filename based on the timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    image_path = f'snapshot_{timestamp}.jpg'
    
    # Save the frame as a JPG image
    cv2.imwrite(image_path, frame)
    
    # Insert the URL and image path into the database
    cursor.execute('INSERT INTO snapshots (url, image_path) VALUES (?, ?)', (url, image_path))
    conn.commit()

def main():
    # Replace 'your_rtsp_urls' with a list of your RTSP URLs
    rtsp_urls = ['rtsp://admin:css12345@10.236.40.208:554/Streaming/channels/101']
    
    for rtsp_url in rtsp_urls:
        # Open the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            print(f'Error: Unable to open RTSP stream for URL: {rtsp_url}')
            continue
        
        ret, frame = cap.read()
        if not ret:
            print(f'Error: Unable to read frame from RTSP stream for URL: {rtsp_url}')
            cap.release()
            continue
        
        # Process and save the frame
        save_snapshot(rtsp_url, frame)
        
        # Display the frame (optional)
        cv2.imshow('Snapshot', frame)
        
        # Release the video capture
        cap.release()
        
        # Press any key to move on to the next URL
        cv2.waitKey(0)
    
    # Close the database connection
    cv2.destroyAllWindows()
    conn.close()

if __name__ == '__main__':
    main()
