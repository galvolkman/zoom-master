import socket
import sounddevice as sd
import numpy as np

# Server configuration
HOST = '0.0.0.0'
PORT = 12345

# Audio configuration
channels = 1
sample_rate = 44100
dtype = np.int16


def receive_audio():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))

        print("Server is listening on {}:{}".format(HOST, PORT))

        with sd.OutputStream(channels=channels, samplerate=sample_rate, dtype=dtype) as stream:
            while True:
                data, addr = server_socket.recvfrom(1024)  # Adjust buffer size as needed
                audio_chunk = np.frombuffer(data, dtype=dtype)
                stream.write(audio_chunk)


if __name__ == "__main__":
    receive_audio()