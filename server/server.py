from datetime import datetime as dt, timedelta as td
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

        print(f"server started on {host}:{port}")
        print(security.access_key, security.offset, time.asctime())

    def admin_panel(self):
        while True:
            command = input()

            try:
                if command == '-clients':
                    if len(self.clients) == 0:
                        print("No connected clients")
                    else:
                        for nickname, address in self.clients.items():
                            print(nickname, address[1])
                    continue

                if command == '-banned':
                    with open('banned_clients.txt', 'r') as file:
                        lines = file.readlines()

                        if len(lines) == 0:
                            print("No banned clients")
                        else:
                            for line in lines:
                                print(line.strip().replace(
                                    '|', " banned until "))

                            print(f"total banned: {len(lines)}")
                        continue

                if command.split()[0] == '-ban':
                    nick = command.split()[1]
                    host = self.clients[nick][1][0]

                    with open('banned_clients.txt', 'a') as file:
                        if len(command.split()) == 2:
                            tBan = dt.max
                            file.write(f"{host}|{dt.max}\n")
                        else:
                            tBan = dt.now() + td(hours=int(command.split()[2]))
                            file.write(f"{host}|{tBan}\n")

                    self.clients[nick][0].send(f"banned {tBan}".encode())

                    print(f"{nick} was banned until {tBan}")
                    continue

                if command.split()[0] == '-unban':
                    host = command.split()[1]

                    with open('banned_clients.txt', 'r') as file:
                        lines = file.readlines()
                        for number, line in enumerate(lines):
                            if host in line:
                                del lines[number]

                            with open('banned_clients.txt', 'w') as file:
                                for line in lines:
                                    file.write(line)

                self.broadcast(command, 'Admin')

            except:
                continue

    def broadcast(self, message: str, nickname: str) -> None:
        for nick, client_socket in self.clients.items():
            if nick == nickname:
                continue

            client_socket[0].send(security.encrypt(f"{nickname}: {message}"))

    def recieve_messages(self, client_socket: socket, nickname: str) -> None:
        while True:
            ban, tBan = self.check_ban(self.clients[nickname][1])

            if ban is True:
                del self.clients[nickname]
                client_socket.close()
                break

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
            ban, tBan = self.check_ban(address)

            if ban is True:
                communication_socket.send(f"banned {tBan}".encode())
                print(f"{address} tried to connect with ban until {tBan}")
                continue

            if security.verify_key(access_key) is True:
                self.clients[nickname] = (communication_socket, address)
                communication_socket.send(f"PK{security.public_key}".encode())

                thread = threading.Thread(
                    target=self.recieve_messages, args=(communication_socket, nickname))
                thread.start()

                print(f"{address} was connected with nickname: {nickname}")
            else:
                print(f"{nickname} entered incorrect access key")
                communication_socket.send('close connection'.encode())
                communication_socket.close()

    def check_ban(self, address) -> set:
        with open('banned_clients.txt', 'r') as file:
            format = '%Y-%m-%d %H:%M:%S.%f'
            lines = file.readlines()
            host = address[0]

            for number, line in enumerate(lines):
                if host in line:
                    time = dt.strptime(line.split('|')[1].strip(), format)
                    if dt.now() >= time:
                        del lines[number]

                        with open('banned_clients.txt', 'w') as file:
                            for line in lines:
                                file.write(line)

                        return (False, dt.now())
                    else:
                        return (True, time)

            return (False, dt.now())


if len(sys.argv) > 1:
    host = socket.gethostbyname(socket.gethostname())
    server = Server(host, int(sys.argv[1]))
else:
    server = Server('localhost', 55555)

admin_thread = threading.Thread(target=server.admin_panel)
admin_thread.start()
server.recieve_connections()
