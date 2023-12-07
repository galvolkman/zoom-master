import cv2
import pickle
from protocol import Protocol  # Assuming you have a custom Protocol class


class Server:
    def __init__(self):
        # Create a Protocol object
        self.socket = Protocol()
        self.socket.bind(("127.0.0.1", 8080))
        # self.socket.listen()
        # self.c_s, _ = self.socket.accept()


        # Open a connection to the default camera (index 0)
        print("a")
        self.vid = cv2.VideoCapture(0)
        print("b")

    def run(self):
        while True:
            # Capture the video frame
            ret, frame = self.vid.read()

            # Serialize the frame using pickle
            serialized_frame = frame.tobytes()

            address = ("127.0.0.2", 8081)
            # Send the serialized frame
            self.socket.send_msg(serialized_frame, address)
            data = self.socket.get_msg()
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