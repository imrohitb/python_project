import cv2

# Replace with your RTSP URL
rtsp_url = "rtsp://admin:css12345@172.55.23.94:554/cam/realmonitor?channel=1&subtype=0"

cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Cannot open stream")
else:
    print("Stream opened successfully!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow('RTSP Stream', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
