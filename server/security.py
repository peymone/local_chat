import string
import random


class Security:
    def __init__(self) -> None:
        self.key_letters = string.ascii_letters + string.digits + string.punctuation
        self.master_key = 'test'

    def generate_key(self):
        self.master_key = ''.join(random.choice(
            self.key_letters) for i in range(5))

    def key_validation(self, master_key) -> bool:
        if self.master_key == master_key:
            return True
