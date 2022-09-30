from cryptography.fernet import Fernet
import random


class Security:
    def __init__(self) -> None:
        """pass offset and acess key verbally, public key programmatically"""
        self.private_key = Fernet.generate_key().decode()
        self.offset = random.randint(0, len(self.private_key) - 5)
        self.access_key = self.private_key[self.offset: self.offset + 5]
        self.public_key = self.private_key[:].replace(self.access_key, '')

        self.fernet = Fernet(self.private_key.encode())

    def verify_key(self, access_key: str) -> bool:
        if self.access_key == access_key:
            return True

    def encrypt(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt(self, message: bytes) -> str:
        return self.fernet.decrypt(message).decode()


security = Security()
