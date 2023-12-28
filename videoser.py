import cv2
import pickle
from protocol import Protocol  # Assuming you have a custom Protocol class
import threading
import numpy as np
import time


class Frame:
    def __init__(self):
        self.img = None

    def setImg(self, img):
        self.img = img

    def getImg(self):
        return self.img


class ClientReader:
    def __init__(self, frame: Frame, pro: Protocol, whoami: int):
        self.frame = frame
        self.pro = pro
        self.whoami = whoami
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                img_frame = pickle.loads(self.pro.get_msg())
                self.frame.setImg(img_frame)
                # print(f"updating {self.whoami}")
            except Exception as e:
                print(f"Error reading from client {self.whoami}: {str(e)}")
                self.stop()


class Server:
    def __init__(self):
        # Create a Protocol object
        self.socket = Protocol()
        self.socket.bind(("0.0.0.0", 8081))
        self.socket.listen()
        self.clients = []
        self.Frames = []
        self.readers = []
        self.running = True

    def images(self):
        arr = [frame.getImg() for frame in self.Frames if frame.getImg() is not None]
        return arr

    def show_video(self):
        while self.running:
            if not all(frame.getImg() is None for frame in self.Frames):
                try:
                    # concatenate image horizontally
                    screen = np.concatenate(self.images(), axis=1)
                    cv2.imshow('screen', screen)

                    # Check for the 'x' key press
                    key = cv2.waitKey(1)
                    if key == ord('x'):
                        self.stop()

                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error displaying video: {str(e)}")

    def stop(self):
        self.running = False
        for reader in self.readers:
            reader.stop()

    def call_run(self):
        for i in range(10):
            pro, addr = self.socket.accept()
            self.Frames.append(Frame())
            self.clients.append(addr)
            print("got new client from", addr)
            client_reader = ClientReader(self.Frames[i], pro, i)
            self.readers.append(client_reader)
            t = threading.Thread(target=client_reader.run)
            t.start()

    def wait_for_exit(self):
        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join()


def main():
    ser = Server()
    threading.Thread(target=ser.show_video).start()
    threading.Thread(target=ser.call_run).start()

    try:
        while ser.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server is shutting down...")
        ser.stop()
        ser.wait_for_exit()


if __name__ == '__main__':
    main()
