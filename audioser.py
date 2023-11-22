import socket
import sounddevice as sd
import numpy as np

# Client configuration
HOST = '127.0.0.1'  # Change to the server's IP address
PORT = 12345

# Audio configuration
channels = 1
sample_rate = 44100
dtype = np.int16

def send_audio():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            with sd.InputStream(channels=channels, samplerate=sample_rate, dtype=dtype) as stream:
                print("Client is sending audio to {}:{}".format(HOST, PORT))
                while True:
                    audio_chunk, overflowed = stream.read(1024)  # Adjust buffer size as needed
                    data = audio_chunk.tobytes()
                    client_socket.sendto(data, (HOST, PORT))
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    send_audio()