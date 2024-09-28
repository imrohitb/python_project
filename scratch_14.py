import cv2
import numpy as np

# Define the RTSP URL
rtsp_url = "rtsp://admin:admin123@172.55.17.41:554/cam/realmonitor?channel=4&subtype=1"

# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Camera not working")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram of the grayscale image
    hist, bins = np.histogram(gray.ravel(), 256, [0, 256])

    # Calculate the standard deviation of the histogram
    std_dev = np.std(hist)

    # Check if the standard deviation is below a certain threshold (e.g., 10)
    if std_dev < 10:
        print("Camera not working")
    else:
        print("Working")

    # Display the frame (optional)
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()