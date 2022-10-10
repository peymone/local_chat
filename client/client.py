import sys
import socket
import threading
from interface import ui
from security import security


class Client:
    def __init__(self, host, port) -> None:
        self.server_host = host
        self.server_port = port
        self.nickname = input("choose a nickname: ")

        # Create a client socket and connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_host, self.server_port))

        # Send first messages with access key and nickname
        self.client.send(f"{security.access_key}>|<".encode())
        self.client.send(self.nickname.encode())

        ui.show_logo()
        ui.show_msg(f"[sys]client started on[/sys] {host}:{port}\n")

    def recieve_message(self):
        while True:
            try:
                message = self.client.recv(1024)
                if message.decode()[:2] == 'PK':
                    security.initialize_fernet(message.decode()[2:])
                    continue
                elif message.decode()[:6] == 'banned':
                    ui.show_msg(
                        f"[sys]you are banned for:[/sys] {message.decode()[6:]}")
                    break
                elif message.decode() == 'close connection':
                    ui.show_msg("[sys]entered incorrect access key")
                    break

                ui.show_msg(security.decrypt(message))
            except:
                ui.show_msg("[sys]server has stopped or you have been banned")
                self.client.close()
                break

    def write_message(self):
        while True:
            try:
                message = input()
                self.client.send(security.encrypt('[clt]' + message))
            except:
                break


if len(sys.argv) > 1:
    client = Client(int(sys.argv[1]), int(sys.argv[2]))
else:
    client = Client('localhost', 55555)

recieve_thread = threading.Thread(target=client.recieve_message)
recieve_thread.start()

write_thread = threading.Thread(target=client.write_message)
write_thread.start()
