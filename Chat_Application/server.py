import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("Server started successfully")
print("Waiting for clients...")
print("IP:", HOST)
print("PORT:", PORT)


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                pass


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()

            if message:
                print(message)
                broadcast(message, client)
            else:
                break

        except:
            break

    remove_client(client)


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)
        client.close()

        print(username, "disconnected")
        broadcast(username + " left the chat")


while True:
    client, address = server.accept()

    print("Client connected:", address)

    client.send("USERNAME".encode())
    username = client.recv(1024).decode()

    clients.append(client)
    usernames.append(username)

    print(username, "joined the chat")

    broadcast(username + " joined the chat", client)

    thread = threading.Thread(
        target=handle_client,
        args=(client,),
        daemon=True
    )

    thread.start()
