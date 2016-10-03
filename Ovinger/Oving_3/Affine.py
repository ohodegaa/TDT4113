__author__ = 'ohodegaa'

from Koder import Cipher
from Multiplicative import MultiplicativeCipher
from Caesar import CaesarCipher
from random import randint


class AffineCipher(Cipher):
    def __init__(self, keys: str = None):
        if keys is not None:
            self.set_key(keys)

    def set_key(self, keys: str = None):
        self.key = eval(str(keys))
        self.multi_coder = MultiplicativeCipher(int(self.key[0]))
        self.caesar_coder = CaesarCipher(int(self.key[1]))

    ### SENDER:
    def encode(self, text: str):
        multi_text = self.multi_coder.encode(text)
        cipher = self.caesar_coder.encode(multi_text)

        return cipher

    def corresponding_key(self):
        return self.multi_coder.corresponding_key(), self.caesar_coder.corresponding_key()

    ### RECEIVER:
    def decode(self, text: str):
        multi_text = self.caesar_coder.decode(text)
        plain_text = self.multi_coder.decode(multi_text)

        return plain_text

    def operate_symbol(self, symbol: chr):
        pass

    def generate_key(self):
        key1 = randint(0, self.DIVISOR)
        key2 = randint(0, self.DIVISOR)
        self.multi_coder.set_key(key1)
        self.caesar_coder.set_key(key2)
        return key1, key2