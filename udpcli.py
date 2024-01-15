from protocol import Protocol
import pickle
import cv2

class Client:
    def __init__(self):
        self.socket = Protocol()
        self.server_addr = ("127.0.0.1", 8081)
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def run(self):
        while True:
            ret, frame = self.vid.read()
            serialized_frame = pickle.dumps(frame)
            self.socket.send_msg(serialized_frame, self.server_addr)

    def release(self):
        self.vid.release()

    def close(self):
        self.socket.close()

def main():
    cli = Client()
    threading.Thread(target=cli.run).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Client is shutting down...")
        cli.close()

if __name__ == '__main__':
    main()
