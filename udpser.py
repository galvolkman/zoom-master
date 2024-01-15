from __future__ import annotations
import socket
import cv2
import pickle
import threading
import numpy as np
import time

class Protocol:
    def __init__(self, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
        self.LENGTH_FIELD_SIZE = 10
        self.socket = sock

    def bind(self, addr: (str, int)):
        return self.socket.bind(addr)

    def close(self):
        self.socket.close()

    def recv_all(self, counter) -> bytes:
        msg = b""
        while len(msg) != counter:
            res, _ = self.socket.recvfrom(counter - len(msg))
            if res == b"":
                print("recv None")
                raise ConnectionError
            msg += res
        return msg

    def get_msg(self):
        length, addr = self.socket.recvfrom(self.LENGTH_FIELD_SIZE)
        length = int(length.decode())
        return self.recv_all(length), addr

    def send_msg(self, data: bytes, addr: (str, int)):
        try:
            self.socket.sendto(str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data, addr)
        except Exception:
            raise

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
                data, _ = self.pro.get_msg()
                img_frame = pickle.loads(data)
                self.frame.setImg(img_frame)
            except Exception as e:
                print(f"Error reading from client {self.whoami}: {str(e)}")
                self.stop()

class Server:
    def __init__(self):
        self.socket = Protocol()
        self.socket.bind(("0.0.0.0", 8081))
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
                    screen = np.concatenate(self.images(), axis=1)
                    cv2.imshow('screen', screen)
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
        while self.running:
            try:
                data, addr = self.socket.get_msg()
                i = len(self.Frames)
                self.Frames.append(Frame())
                self.clients.append(addr)
                print("got new client from", addr)
                client_reader = ClientReader(self.Frames[i], self.socket, i)
                self.readers.append(client_reader)
                t = threading.Thread(target=client_reader.run)
                t.start()
            except KeyboardInterrupt:
                self.stop()

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
