import cv2
import pickle
from protocol import Protocol  # Assuming you have a custom Protocol class

# Create a Protocol object
socket = Protocol()
socket.bind(("127.0.0.1", 8080))
socket.listen()
c_s, _ = socket.accept()

# Open a connection to the default camera (index 0)
vid = cv2.VideoCapture(0)

while True:
    # Capture the video frame
    ret, frame = vid.read()

    # Serialize the frame using pickle
    serialized_frame = pickle.dumps(frame)

    # Send the serialized frame
    c_s.send_msg(serialized_frame)

    # Display the frame
    cv2.imshow('frame', frame)

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
vid.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()

# Close the socket
c_s.close()
