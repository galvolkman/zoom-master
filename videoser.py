import cv2
from protocol import Protocol
from scipy.io import loadmat


socket = Protocol()
socket.bind(("127.0.0.1", 8080))
socket.listen()
c_s, _ = socket.accept()
# import the opencv library
# define a video capture object
vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    c_s.send_msg(frame)
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
