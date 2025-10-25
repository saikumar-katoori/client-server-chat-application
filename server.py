# import socket
# import threading

# HOST = '127.0.0.1'
# PORT = 12345

# clients = []
# usernames = {}

# # Broadcast to all clients
# def broadcast(message, sender_socket=None):
#     for client in clients:
#         if client != sender_socket:
#             try:
#                 client.send(message.encode('utf-8'))
#             except:
#                 clients.remove(client)

# # Handle client messages
# def handle_client(client_socket):
#     try:
#         username = client_socket.recv(1024).decode('utf-8')
#         usernames[client_socket] = username
#         print(f"{username} joined the chat.")
#         broadcast(f"{username} joined the chat!", client_socket)
        
#         while True:
#             message = client_socket.recv(1024).decode('utf-8')
#             if message:
#                 full_message = f"{username}: {message}"
#                 print(full_message)
#                 broadcast(full_message, client_socket)
#     except:
#         clients.remove(client_socket)
#         print(f"{usernames[client_socket]} left the chat.")
#         broadcast(f"{usernames[client_socket]} left the chat.", client_socket)
#         client_socket.close()

# # Allow server to send messages
# def server_send():
#     while True:
#         msg = input()  # Type message in server console
#         full_message = f"Server: {msg}"
#         print(full_message)
#         broadcast(full_message)

# # Start server
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen()
# print(f"Server listening on {HOST}:{PORT}")

# # Start server sending thread
# threading.Thread(target=server_send, daemon=True).start()

# while True:
#     client_socket, addr = server.accept()
#     clients.append(client_socket)
#     thread = threading.Thread(target=handle_client, args=(client_socket,))
#     thread.start()


import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

clients = []
usernames = {}

# Broadcast messages to all clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

# Add message to server GUI and log
def add_message(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"[{timestamp}] {message}\n")
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')
    
    # Optional: log to file
    with open("server_chat_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# Handle each client
def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        join_msg = f"{username} joined the chat"
        add_message(join_msg)
        broadcast(join_msg, client_socket)
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                full_message = f"{username}: {message}"
                add_message(full_message)
                broadcast(full_message, client_socket)
    except:
        clients.remove(client_socket)
        leave_msg = f"{usernames[client_socket]} left the chat"
        add_message(leave_msg)
        broadcast(leave_msg, client_socket)
        client_socket.close()

# Send messages from server GUI
def send_message():
    message = message_var.get()
    if message:
        full_message = f"Server: {message}"
        add_message(full_message)
        broadcast(full_message)
        message_var.set("")

# Accept clients continuously
def accept_clients():
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("Server Chat")

chat_area = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20)
chat_area.pack(padx=10, pady=10)

message_var = tk.StringVar()
message_entry = tk.Entry(root, textvariable=message_var, width=40)
message_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

# Networking setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
add_message(f"Server listening on {HOST}:{PORT}")

threading.Thread(target=accept_clients, daemon=True).start()
root.mainloop()
