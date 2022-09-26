import socket
import threading


class Client:
    def __init__(self, host, port) -> None:
        self.server_host = host
        self.server_port = port
        self.master_key = input("Enter your master key: ") + '>|<'
        self.nickname = input("Choose a nickname: ")

        # Create a client socket and connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_host, self.server_port))

        # Send first messages with master key and nickname
        self.client.send(self.master_key.encode('utf-8'))
        self.client.send(self.nickname.encode('utf-8'))

    def recieve_message(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'close':
                    print("entered incorrect master key")
                    break

                print(message)
            except:
                self.client.close()

                print("server has stopped")
                break

    def write_message(self):
        while True:
            try:
                message = input()
                self.client.send(message.encode('utf-8'))
            except:
                break


client = Client('localhost', 55555)
recieve_thread = threading.Thread(target=client.recieve_message)
recieve_thread.start()

write_thread = threading.Thread(target=client.write_message)
write_thread.start()
