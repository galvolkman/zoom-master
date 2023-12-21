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
    def __init__(self, frame: Frame, pro : Protocol, whoami: int):
        self.frame = frame
        self.pro = pro
        self.whoami = whoami

    def run(self):

        while True:
            img_frame = pickle.loads(self.pro.get_msg())
            self.frame.setImg(img_frame)
            print(f"updating {self.whoami}")


class Server:
    def __init__(self):
        # Create a Protocol object
        self.socket = Protocol()
        self.socket.bind(("0.0.0.0", 8080))
        self.socket.listen()
        self.clients = []
        self.Frames = [Frame(), Frame()]
        self.readers = []


    def show_video(self):
        while (self.Frames[0].getImg() is None) or (self.Frames[1].getImg() is None):
            pass
        while True:


            # concatenate image Horizontally
            screen = np.concatenate((self.Frames[0].getImg(), self.Frames[1].getImg()), axis=1)
            cv2.imshow('screen', screen)
            time.sleep(0.1)

    def call_run(self):

        for i in range(2):
            pro, _ = self.socket.accept()
            client_reader = ClientReader(self.Frames[i], pro, i)
            self.readers.append(client_reader)

            t = threading.Thread(target=client_reader.run)
            t.start()




def main():
    ser = Server()
    ser.call_run()
    threading.Thread(target=ser.show_video).start()

    #cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
