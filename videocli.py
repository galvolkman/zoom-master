from protocol import Protocol
import pickle
import cv2


class Client:
    def __init__(self):
        self.socket = Protocol()
        self.socket.connect(("127.0.0.1", 8080))
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def run(self):
        while True:
            # Capture the video frame
            ret, frame = self.vid.read()

            # Serialize the frame using pickle
            serialized_frame = pickle.dumps(frame)

            # Send the serialized frame
            self.socket.send_msg(serialized_frame)

            # Display the frame
            # cv2.imshow('frame', frame)

            # Check for the 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def relese(self):
        # Release the video capture object
        self.vid.release()

    def close(self):

        # Close the socket
        self.socket.close()


def main():
    cli = Client()
    cli.run()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()