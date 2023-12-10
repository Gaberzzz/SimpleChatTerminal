import threading
import time, socket, sys
# Receive messages
def receive_messages(soc):
   while True:
      message = soc.recv(1024) 
      message = message.decode()  
      print(server_name, ">", message)
print('Client Server...')
time.sleep(1)

#Get the hostname, IP Address from socket 
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)

#get information to connect with the server
print(shost, '({})'.format(ip))

#Setting up names and connection and port
server_host = input('Enter server\'s IP address:')
name = input('Enter Client\'s name: ')
port = 1234

#Connecting to Server
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Connected...")
soc.send(name.encode())

#listening to server
server_name = soc.recv(1024)
server_name = server_name.decode()
print('{} has joined...'.format(server_name))

recv_thread = threading.Thread(target=receive_messages, args=(soc,)) 
recv_thread.start()

while True:
   message = input("Me > ")
   if message == "[bye]":
     message = "Leaving the Chat room"
     soc.send(message.encode()) 
     break

   soc.send(message.encode())