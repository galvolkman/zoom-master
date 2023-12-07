from protocol import Protocol
import pickle
import cv2
import numpy


class Client:
    def __init__(self):
        self.socket = Protocol()
        self.socket.bind(("127.0.0.2", 8081))
        # import the opencv library

# define a video capture object

    def run(self):
        while (True):

            # Capture the video frame
            # by frame

            data = self.socket.get_msg()
            frame = numpy.frombuffer(data)

            # Display the resulting frame
            cv2.imshow('frame', frame)
            self.socket.send_msg("gotaframe", ("127.0.0.1", 8080))

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # After the loop release the cap object

        # Destroy all the windows
        cv2.destroyAllWindows()


def main():
    cli = Client()
    cli.run()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()