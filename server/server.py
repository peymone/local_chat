from security import security
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
        else:
            print(f"server is running in test mode! {host}:{port}")

        print(
            f"access key: {security.access_key}, offset: {security.offset}, time: {time.asctime()}")

    def admin_panel(self):
        while True:
            command = input()
            self.broadcast(command, 'Admin')

    def broadcast(self, message: str, nickname: str) -> None:
        for nick, client_socket in self.clients.items():
            if nick == nickname:
                continue

            client_socket.send(security.encrypt(f"{nickname}: {message}"))

    def recieve_messages(self, client_socket: socket, nickname: str) -> None:
        while True:
            try:
                message = security.decrypt(client_socket.recv(1024))
                self.broadcast(message, nickname)
                print(f"{nickname}: {message}")
            except:
                del self.clients[nickname]
                client_socket.close()

                print(f"{nickname} left the chat")
                break

    def recieve_connections(self):
        """Waiting for connetcions and recieve first messages"""

        while True:
            communication_socket, address = self.server.accept()
            buffer = communication_socket.recv(1024).decode()
            access_key = buffer.split('>|<')[0]
            nickname = buffer.split('>|<')[1]

            print(f"{address} trying to connect with nickname: {nickname}")
            if security.verify_key(access_key) == True:
                self.clients[nickname] = communication_socket
                communication_socket.send(f"PK{security.public_key}".encode())

                thread = threading.Thread(
                    target=self.recieve_messages, args=(communication_socket, nickname))
                thread.start()

                print(f"{address} was connected with nickname: {nickname}")
            else:
                print(f"{nickname} entered incorrect access key")
                communication_socket.send('close connection'.encode())
                communication_socket.close()


if len(sys.argv) > 1:
    host = socket.gethostbyname(socket.gethostname())
    server = Server(host, int(sys.argv[1]))
else:
    server = Server('localhost', 55555)

admin_thread = threading.Thread(target=server.admin_panel)
admin_thread.start()
server.recieve_connections()
