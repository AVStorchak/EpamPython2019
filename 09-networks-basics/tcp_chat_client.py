import socket
import sys
import threading


def receive():
    while True:
        try:
            in_message = client.recv(512).decode("utf8")
            print(f'{in_message}')
        except TypeError:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5090))
threading.Thread(target=receive).start()
out_message = ''

while out_message != "!quit":
    out_message = input('[You]: ')
    client.send(bytes(out_message, "utf8"))

client.close()
