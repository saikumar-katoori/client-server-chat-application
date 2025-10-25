# import socket
# import threading
# import tkinter as tk
# from tkinter import scrolledtext
# import random

# HOST = '127.0.0.1'
# PORT = 12345

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))

# # Ask for username
# username = input("Enter your username: ")
# client.send(username.encode('utf-8'))

# # Tkinter GUI
# root = tk.Tk()
# root.title(f"Chat - {username}")

# chat_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
# chat_area.pack(padx=10, pady=10)

# message_var = tk.StringVar()
# message_entry = tk.Entry(root, textvariable=message_var, width=40)
# message_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

# def send_message():
#     message = message_var.get()
#     if message:
#         client.send(message.encode('utf-8'))
#         message_var.set("")

# send_button = tk.Button(root, text="Send", command=send_message)
# send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

# # Assign a random color for each user
# user_colors = {}

# def receive_messages():
#     while True:
#         try:
#             message = client.recv(1024).decode('utf-8')
#             if message:
#                 # Extract username from message if possible
#                 if ": " in message:
#                     sender, text = message.split(": ", 1)
#                     if sender not in user_colors:
#                         user_colors[sender] = random.choice([
#                             "red","green","blue","orange","purple","brown"
#                         ])
#                     color = user_colors[sender]
#                     chat_area.config(state='normal')
#                     chat_area.insert(tk.END, f"{sender}: ", ('color',))
#                     chat_area.insert(tk.END, f"{text}\n")
#                     chat_area.tag_config('color', foreground=color)
#                     chat_area.yview(tk.END)
#                     chat_area.config(state='disabled')
#                 else:
#                     # System messages
#                     chat_area.config(state='normal')
#                     chat_area.insert(tk.END, message + "\n")
#                     chat_area.yview(tk.END)
#                     chat_area.config(state='disabled')
#         except:
#             break

# threading.Thread(target=receive_messages, daemon=True).start()

# root.mainloop()
##########################

# import socket
# import threading
# import tkinter as tk
# from tkinter import scrolledtext
# import random

# HOST = '127.0.0.1'
# PORT = 12345

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))

# # Ask for username
# username = input("Enter your username: ")
# client.send(username.encode('utf-8'))

# # GUI setup
# root = tk.Tk()
# root.title(f"Chat - {username}")

# chat_area = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20)
# chat_area.pack(padx=10, pady=10)

# message_var = tk.StringVar()
# message_entry = tk.Entry(root, textvariable=message_var, width=40)
# message_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

# def send_message():
#     message = message_var.get()
#     if message:
#         client.send(message.encode('utf-8'))
#         message_var.set("")

# send_button = tk.Button(root, text="Send", command=send_message)
# send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

# user_colors = {}

# # Receive messages from server
# def receive_messages():
#     while True:
#         try:
#             message = client.recv(1024).decode('utf-8')
#             if message:
#                 if ": " in message:
#                     sender, text = message.split(": ", 1)
#                     if sender not in user_colors:
#                         user_colors[sender] = random.choice([
#                             "red","green","blue","orange","purple","brown"
#                         ])
#                     color = user_colors[sender]
#                     chat_area.config(state='normal')
#                     chat_area.insert(tk.END, f"{sender}: ", ('color',))
#                     chat_area.insert(tk.END, f"{text}\n")
#                     chat_area.tag_config('color', foreground=color)
#                     chat_area.yview(tk.END)
#                     chat_area.config(state='disabled')
#                 else:
#                     # System messages
#                     chat_area.config(state='normal')
#                     chat_area.insert(tk.END, message + "\n")
#                     chat_area.yview(tk.END)
#                     chat_area.config(state='disabled')
#         except:
#             break

# threading.Thread(target=receive_messages, daemon=True).start()
# root.mainloop()
#####################

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import random

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Ask for username
username = input("Enter your username: ")
client.send(username.encode('utf-8'))

# GUI setup
root = tk.Tk()
root.title(f"Chat - {username}")

chat_area = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20)
chat_area.pack(padx=10, pady=10)

message_var = tk.StringVar()
message_entry = tk.Entry(root, textvariable=message_var, width=40)
message_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

user_colors = {}

# Function to add messages to chat area
def add_message(message, sender=None):
    chat_area.config(state='normal')
    if sender:
        if sender not in user_colors:
            user_colors[sender] = random.choice([
                "red","green","blue","orange","purple","brown"
            ])
        color = user_colors[sender]
        chat_area.insert(tk.END, f"{sender}: ", ('color',))
        chat_area.insert(tk.END, f"{message}\n")
        chat_area.tag_config('color', foreground=color)
    else:
        # System messages
        chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')

# Send message function
def send_message():
    message = message_var.get()
    if message:
        client.send(message.encode('utf-8'))
        add_message(message, username)  # Display own message
        message_var.set("")

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

# Receive messages from server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                # Avoid duplicating own messages
                if message.startswith(f"{username}: "):
                    continue
                if ": " in message:
                    sender, text = message.split(": ", 1)
                    add_message(text, sender)
                else:
                    add_message(message)  # System message
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()
root.mainloop()
