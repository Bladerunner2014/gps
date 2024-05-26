import random
import string
import time


class IDGenerator:
    def __init__(self, prefix):
        self.prefix = prefix

    def generate_custom_id(self):
        timestamp = str(int(time.time()))
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{self.prefix}-{timestamp}-{random_chars}"
