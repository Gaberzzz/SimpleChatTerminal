import threading
import tkinter as tk
from tkinter import scrolledtext
import socket
import time

def handle_client(client_socket, client_name, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == '[bye]':
                print(f"{client_name} has left the chat.")
                break
            print(f"{client_name} > {message}")
            text_area.insert(tk.END, f"{client_name} > {message}\n")
            broadcast(f"{client_name} > {message}", client_socket)

        except:
            print(f"Connection with {client_name} lost.")
            break

def receive_messages():
    while True:
        for client_socket, client_name in clients:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"{client_name} > {message}")
                    text_area.insert(tk.END, f"{client_name} > {message}\n")
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

def start_server_gui():
    window = tk.Tk()
    window.title('Server Chat')

    global text_area
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
    text_area.grid(column=0, row=0, columnspan=2)

    server_send_entry = tk.Entry(window, width=30)
    server_send_entry.grid(column=0, row=1)

    server_send_button = tk.Button(window, text='Send', command=lambda: send_to_all_gui(server_send_entry))
    server_send_button.grid(column=1, row=1)

    def send_to_all_gui(entry):
        message = entry.get()
        text_area.insert(tk.END, f'Server > {message}\n')
        entry.delete(0, tk.END)
        send_to_all(f"Server > {message}")

    window.mainloop()

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

# Start the server GUI in a separate thread
server_gui_thread = threading.Thread(target=start_server_gui)
server_gui_thread.start()

# Start the receive thread
recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

while True:
    client_socket, addr = soc.accept()
    print("Received connection from ", addr[0], "(", addr[1], ")")
    print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))

    client_name = client_socket.recv(1024).decode()
    print(client_name + ' has connected.\n')
    client_socket.send(name.encode())

    clients.append((client_socket, client_name))

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name, text_area))
    client_handler.start()

    # Notify all clients about the new connection
    send_to_all(f"{client_name} has joined the chat.")
