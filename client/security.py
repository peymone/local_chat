from cryptography.fernet import Fernet
import random


class Security:
    def __init__(self) -> None:
        """pass offset and acess key verbally, public key programmatically"""
        self.access_key = input("Enter your access key: ")
        self.offset = int(input("Enter your offset: "))
        self.private_key = ''
        self.public_key = ''

    def initialize_fernet(self, public_key: str) -> None:
        self.private_key = public_key[:self.offset] + \
            self.access_key + public_key[self.offset:]

        self.public_key = public_key
        self.fernet = Fernet(self.private_key.encode())

    def encrypt(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt(self, message: bytes) -> str:
        return self.fernet.decrypt(message).decode()


security = Security()
