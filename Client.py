import threading
import tkinter as tk
from tkinter import scrolledtext
import socket
import time

def receive_messages(soc, text_area):
    while True:
        message = soc.recv(1024)
        message = message.decode()
        text_area.insert(tk.END, f'{server_name} > {message}\n')

def send_message():
    message = message_entry.get()
    text_area.insert(tk.END, f'Me > {message}\n')
    soc.send(message.encode())
    message_entry.delete(0, tk.END)

# Get the hostname, IP Address from the socket
shost = socket.gethostname()
ip = socket.gethostbyname(shost)

# Setting up names and connection and port
server_host = input('Enter server\'s IP address:')
name = input('Enter Client\'s name: ')
port = 1234

# Connecting to the server
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc = socket.socket()
soc.connect((server_host, port))
print("Connected...")
soc.send(name.encode())

# Listening to the server
server_name = soc.recv(1024)
server_name = server_name.decode()
print('{} has joined...'.format(server_name))

# Create the GUI window
window = tk.Tk()
window.title('Chat Application')

# Create and configure text area for messages
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
text_area.grid(column=0, row=0, columnspan=2)

# Create and configure entry for typing messages
message_entry = tk.Entry(window, width=30)
message_entry.grid(column=0, row=1)

# Create and configure send button
send_button = tk.Button(window, text='Send', command=send_message)
send_button.grid(column=1, row=1)

# Start a thread for receiving messages
recv_thread = threading.Thread(target=receive_messages, args=(soc, text_area))
recv_thread.start()

# Run the GUI main loop
window.mainloop()
