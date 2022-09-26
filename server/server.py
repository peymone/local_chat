from security import Security
import threading
import socket
import time
import sys


class Server:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.clients = {}

        # Create a server socket and enable listen mode
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        if self.host == 'localhost':
            print(f"server is running in test mode! {host}:{port}")
            print(f"master key: {security.master_key}, time: {time.asctime()}")
        else:
            print(f"server is running in test mode! {host}:{port}")
            print(f"master key: {security.master_key}, time: {time.asctime()}")

    def broadcast(self, message, nickname):
        for nick, client_socket in self.clients.items():
            if nick == nickname:
                continue

            client_socket.send(f"{nickname}: {message}".encode('utf-8'))

    def recieve_messages(self, client_socket, nickname):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                self.broadcast(message, nickname)
            except:
                del self.clients[nickname]
                client_socket.close()

                print(f"{nickname} left the chat")
                break

    def recieve_connections(self):
        """Waiting for connetcions and recieve first messages"""

        while True:
            communication_socket, address = self.server.accept()
            buffer = communication_socket.recv(1024).decode('utf-8')
            master_key = buffer.split('>|<')[0]
            nickname = buffer.split('>|<')[1]

            print(f"{address} trying to connect with nickname: {nickname}")
            if security.key_validation(master_key) == True:
                self.clients[nickname] = communication_socket

                thread = threading.Thread(
                    target=self.recieve_messages, args=(communication_socket, nickname))
                thread.start()

                print(f"{address} was connected with nickname: {nickname}")
            else:
                print(f"{nickname} entered incorrect master key")
                communication_socket.send('close'.encode('utf-8'))
                communication_socket.close()


if len(sys.argv) > 1:
    security = Security()
    security_thread = threading.Thread(target=security.auto_generate_key)
    security_thread.start()

    host = socket.gethostbyname(socket.gethostname())
    server = Server(host, sys.argv[1])
else:
    security = Security()
    server = Server('localhost', 55555)

server.recieve_connections()
