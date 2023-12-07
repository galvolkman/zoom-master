from __future__ import annotations
import socket


class Protocol:
    def __init__(self, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
        self.LENGTH_FIELD_SIZE = 10
        self.socket = sock

    def connect(self, addr: (str, int)):
        return self.socket.connect(addr)

    def settimeout(self, value):
        return self.socket.settimeout(value)

    def bind(self, addr: (str, int)):
        return self.socket.bind(addr)

    # def listen(self):
    #     return self.socket.listen()

    def close(self):
        self.socket.close()

    # def accept(self):
    #     sock, addr = self.socket.accept()
    #     return Protocol(sock), addr


    def recv_all(self, counter) -> bytes:
        msg = b""
        chunk = 1024
        #print(f"length inside = {counter}")
        while len(msg) < counter:
            toread = min(chunk, counter - len(msg))
            res, address_from = self.socket.recvfrom(toread)
            if res == b"":
                #print("recv None")
                raise ConnectionError
            msg += res
            #print(len(msg))
        return msg

    def get_msg(self, timeout=None):

        #self.socket.settimeout(timeout)
        length = self.recv_all(self.LENGTH_FIELD_SIZE)
        return self.recv_all(int(length))

    def send_msg(self, data: bytes, address):
        try:

            chunk = 1024
            self.socket.sendto(str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode(), address)
            for dlen in range(0, len(data), chunk):
                st = dlen
                end = min(dlen + chunk, len(data))
                self.socket.sendto(data[st:end], address)
        except Exception:
            raise
