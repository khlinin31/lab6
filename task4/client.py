import logging
import socket
import threading
import tkinter as tk


class MessageReceiver(threading.Thread):

    def __init__(self, sock: socket.socket, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None
        self.isOpen = True

    def run(self):
        while self.isOpen:
            message = self.sock.recv(1024).decode('utf-8')

            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)


class Client:

    def __init__(self, host='localhost', port=1337):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
        self.receive = None

    def start(self):
        print(f"Trying to connect to {self.host}:{self.port}...")
        self.sock.connect((self.host, self.port))
        print(f'Successfully connected to {self.host}:{self.port}')

        print()
        self.name = input('Your name: ')

        self.receive = MessageReceiver(self.sock, self.name)
        self.receive.start()

        self.sock.sendall(f'Server: {self.name} has joined the chat. Say hi!'.encode('utf-8'))

        return self.receive

    def send(self, text_input):
        message = text_input.get()
        text_input.delete(0, tk.END)
        self.messages.insert(tk.END, f'{self.name}: {message}')
        self.sock.sendall(f'{self.name}: {message}'.encode('utf-8'))

    def close(self):
        self.sock.sendall(f'Server: {self.name} has left the chat'.encode('ascii'))
        self.sock.close()
