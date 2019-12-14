import socket
import sys
import threading


def send_participants(client):
    participant_names = list(list_of_participants.values())
    participants = ', '.join(participant_names)
    client.send(bytes(participants, "utf8"))


def send_private_msg(client, msg):
    for target, name in list_of_participants.items():
        if msg.startswith(f'!{name}'):
            msg_to_send = f'From {list_of_participants[client]}: ' + msg[(len(name)+2):]
            target.send(bytes(msg_to_send, "utf8"))


def broadcast(message, client):
    for particpant in list_of_participants:
        if particpant != client:
                try:
                    particpant.send(message)
                except:
                    del list_of_participants[particpant]


def run_client(client, address):

    client.send(b"Welcome! What is your name?\n")
    client.send(b"Send '!quit' to quit the chat\n")
    client.send(b"Send '!get_list' to get the list of participants\n")
    client.send(b"Send '!<participant_name>' + message to send a private message to this participant\n")
    name = client.recv(512).decode("utf8")
    list_of_participants[client] = name.strip()
    new_user_notification = (f'{name} has joined the chat!')
    user_left_notification = (f'{name} has left the chat!')
    broadcast(str.encode(new_user_notification), client)
    print(list_of_participants)

    while True:
        try:
            message = client.recv(512).decode("utf8")
            if message == '!quit':
                print(user_left_notification)
                broadcast(str.encode(user_left_notification), client)
                del list_of_participants[client]
                break
            elif message == '!get_list':
                send_participants(client)
            elif message.startswith('!'):
                send_private_msg(client, message)
            else:
                print(f'{name}: {message}')
                chat_message = f'[{name}]: {message}'
                broadcast(str.encode(chat_message), client)

        except:
            print(user_left_notification)
            broadcast(str.encode(user_left_notification), client)
            del list_of_participants[client]
            print(list_of_participants)
            break

chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind(('localhost', 5090))
chat_server.listen(5)
list_of_participants = {}
print("Chat server is running")

while True:
    clientsocket, clientaddress = chat_server.accept()
    list_of_participants[clientsocket] = ''
    print(clientaddress, "has connected")
    threading.Thread(target=run_client, args=(clientsocket, clientaddress)).start()
