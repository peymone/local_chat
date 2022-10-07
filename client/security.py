from cryptography.fernet import Fernet


class Security:
    def __init__(self) -> None:
        self.access_key = input("enter your access key: ")
        self.offset = int(input("enter your offset: "))
        self.private_key = ''

    def initialize_fernet(self, public_key: str) -> None:
        self.private_key = public_key[:self.offset] + \
            self.access_key + public_key[self.offset:]

        self.fernet = Fernet(self.private_key.encode())

    def encrypt(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt(self, message: bytes) -> str:
        return self.fernet.decrypt(message).decode()


security = Security()
