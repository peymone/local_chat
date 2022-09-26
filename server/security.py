import string
import random
import time


class Security:
    def __init__(self) -> None:
        self.key_letters = string.ascii_letters + string.digits
        self.master_key = 'test'

    def auto_generate_key(self):
        while True:
            self.master_key = ''.join(
                random.choice(self.key_letters) for i in range(5))

            print(f"master key: {self.master_key}, time: {time.asctime()}")
            time.sleep(60)

    def generate_key(self):
        self.master_key = ''.join(random.choice(
            self.key_letters) for i in range(5))

        print(f"master key: {self.master_key}")

    def key_validation(self, master_key) -> bool:
        if self.master_key == master_key:
            return True
