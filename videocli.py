from protocol import Protocol

socket = Protocol()
socket.connect(("127.0.0.1", 8080))
# import the opencv library
import cv2

# define a video capture object


while (True):

    # Capture the video frame
    # by frame

    frame = socket.get_msg()
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object

# Destroy all the windows
cv2.destroyAllWindows()
