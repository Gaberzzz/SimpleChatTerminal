import threading
import time
import socket

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == '[bye]':
                print(f"{client_name} has left the chat.")
                break
            print(f"{client_name} > {message}")
            broadcast(f"{client_name} > {message}", client_socket)
        except:
            print(f"Connection with {client_name} lost.")
            break

def broadcast(message, current_client_socket):
    for client, name in clients:
        if client != current_client_socket:
            try:
                client.send(message.encode())
            except:
                print(f"Connection with {name} lost.")

def send_to_all(message):
    for client, name in clients:
        try:
            client.send(message.encode())
        except:
            print(f"Connection with {name} lost.")

def server_send():
    while True:
        message = input("Server > ")
        send_to_all(f"Server > {message}")

print('Server turning on')
time.sleep(1)

soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 1234
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))
name = "Referee"

soc.listen()
print('Waiting for incoming connections...\n')

clients = []

while True:
    client_socket, addr = soc.accept()
    print("Received connection from ", addr[0], "(", addr[1], ")")
    print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))

    client_name = client_socket.recv(1024).decode()
    print(client_name + ' has connected.\n')
    client_socket.send(name.encode())

    clients.append((client_socket, client_name))

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
    client_handler.start()

    # Notify all clients about the new connection
    send_to_all(f"{client_name} has joined the chat.")

    # Start a thread for the server to send messages
    server_send_thread = threading.Thread(target=server_send)
    server_send_thread.start()
