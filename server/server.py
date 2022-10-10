from datetime import datetime as dt, timedelta as td
from security import security
from interface import ui
import threading
import socket
import sys

import openpyxl


class Server:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.clients = {}
        self.tFormat = "%d.%m.%Y %H:%M:%S"

        # Create a server socket and enable listen mode
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        ui.show_logo()
        ui.show_msg(f"[sys]server started on[/sys] {host}: {port}")
        ui.show_msg(f"[sys]acess key:[/sys] {security.access_key}")
        ui.show_msg(f"[sys]offset:[/sys] {security.offset}\n")

        self.log(('server', self.tNow, f"server started on {host}:{port}"))
        self.log(('server', self.tNow,
                 f"aKey: {security.access_key}, offset: {security.offset}"))

    @property
    def tNow(self):
        return dt.now().strftime(self.tFormat)

    def admin_panel(self):
        commands = {
            "-clients": "show list of connected clients",
            "-ban client_nickname [hours]": "ban client permanently or for hours (optional)",
            "-unban host": "unban client by host",
            "-banned": "show list of banned clients",
        }

        while True:
            command = input()

            try:
                if command == '-commands' or command == '-help':
                    for cmd, description in commands.items():
                        ui.show_msg(f"[adm]{cmd}: {description}")

                    self.log(('admin', self.tNow, command))
                    continue

                if command == '-clients':
                    if len(self.clients) == 0:
                        ui.show_msg("[adm]no connected clients")
                    else:
                        for nickname, address in self.clients.items():
                            ui.show_msg(f"[adm]{nickname} {address[1]}")

                    self.log(('admin', self.tNow, command))
                    continue

                if command == '-banned':
                    with open('banned_clients.txt', 'r') as file:
                        lines = file.readlines()

                        if len(lines) == 0:
                            ui.show_msg("[adm]no banned clients")
                        else:
                            for line in lines:
                                ui.show_msg(
                                    '[adm]' + line.strip().replace('|', " banned until "))

                            ui.show_msg(f"[adm]total banned: {len(lines)}")

                    self.log(('admin', self.tNow, command))
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
                    self.broadcast(
                        f"[adm]{nick} was banned until[/adm] {tBan}", 'admin')

                    ui.show_msg(f"[adm]{nick} was banned until[/adm] {tBan}")
                    self.log(('admin', self.tNow, command))
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

                    ui.show_msg(f"[adm]{host} was unbanned")
                    self.log(('admin', self.tNow, command))

                    continue

                self.log(('admin', self.tNow, command))
                self.broadcast('[adm]' + command, 'admin')

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
                self.log((nickname, self.tNow, message[5:]))
                self.broadcast(message, nickname)

                ui.show_msg(f"{nickname}: {message}")
                # print(f"{nickname}: {message}")

            except:
                del self.clients[nickname]
                client_socket.close()

                self.log(('server', self.tNow, f"{nickname} left the chat"))
                self.broadcast(f"[sys]{nickname} left the chat", 'server')
                ui.show_msg(f"[sys]{nickname} left the chat")
                # print(f"{nickname} left the chat")
                break

    def recieve_connections(self):
        """Waiting for connetcions and recieve first messages"""

        while True:
            communication_socket, address = self.server.accept()
            buffer = communication_socket.recv(1024).decode()
            access_key = buffer.split('>|<')[0]
            nickname = buffer.split('>|<')[1]

            ban, tBan = self.check_ban(address)
            if ban is True:
                msg = f"{address} tried to connect with ban until {tBan}"
                communication_socket.send(f"banned {tBan}".encode())
                self.log(('server', self.tNow, msg))

                ui.show_msg('[sys]' + msg)
                continue

            if security.verify_key(access_key) is True:
                self.clients[nickname] = (communication_socket, address)
                communication_socket.send(f"PK{security.public_key}".encode())

                thread = threading.Thread(
                    target=self.recieve_messages, args=(communication_socket, nickname))
                thread.start()

                msg = f"{address} was connected with nickname: {nickname}"
                self.broadcast(f"[sys]{nickname} connected", 'server')
                self.log(('server', self.tNow, msg))
                ui.show_msg('[sys]' + msg)

            else:
                communication_socket.send('close connection'.encode())
                communication_socket.close()

                msg = f"{nickname} entered incorrect access key"
                self.log(('server', self.tNow, msg))
                ui.show_msg('[sys]' + msg)

    def check_ban(self, address) -> tuple:
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

    def log(self, data: tuple) -> None:
        book = openpyxl.load_workbook('logs.xlsx')
        sheet = book.active
        sheet.append(data)
        book.save('logs.xlsx')
        book.close()


if len(sys.argv) > 1:
    host = socket.gethostbyname(socket.gethostname())
    server = Server(host, int(sys.argv[1]))
else:
    server = Server('localhost', 55555)

admin_thread = threading.Thread(target=server.admin_panel)
admin_thread.start()
server.recieve_connections()
