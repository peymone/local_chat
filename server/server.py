import socket
import threading


class Server:
    def __init__(self, host, port) -> None:
        # self.host = socket.gethostbyname(socket.gethostname())
        self.host = host
        self.port = port
        self.clients = {}

        # Create a server socket and enable listen mode
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print("Server is running!")

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
            nickname = communication_socket.recv(1024).decode('utf-8')
            self.clients[nickname] = communication_socket

            thread = threading.Thread(
                target=self.recieve_messages, args=(communication_socket, nickname))
            thread.start()

            print(f"{address} was connected with nickname: {nickname}")


server = Server('localhost', 55555)
server.recieve_connections()
