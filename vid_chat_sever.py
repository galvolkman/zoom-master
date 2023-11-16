import cv2
import pickle
from protocol import Protocol  # Assuming you have a custom Protocol class


class Server:
    def __init__(self):
        # Create a Protocol object
        self.socket = Protocol()
        self.socket.bind(("0.0.0.0", 8080))
        self.socket.listen()
        self.c_s, _ = self.socket.accept()


        # Open a connection to the default camera (index 0)
        print("a")
        self.vid = cv2.VideoCapture(0)
        print("b")

    def run(self):
        while True:
            # Capture the video frame
            ret, frame = self.vid.read()

            # Serialize the frame using pickle
            serialized_frame = pickle.dumps(frame)

            # Send the serialized frame
            self.c_s.send_msg(serialized_frame)

            # Display the frame
            #cv2.imshow('frame', frame)

            # Check for the 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def relese(self):
        # Release the video capture object
        self.vid.release()

    def close(self):


        # Close the socket
        self.c_s.close()


def main():
        ser = Server()
        ser.run()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()