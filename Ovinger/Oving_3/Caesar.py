__author__ = 'ohodegaa'
from Koder import Cipher


class CaesarCipher(Cipher):
    def __init__(self, key: int = None):
        if key is not None:
            self.set_key(key)

    def set_key(self, key):
        self.key = int(key)

    def operate_symbol(self, symbol: chr):
        i = Cipher.to_index(symbol)
        i_encoded = (i + self.key) % self.DIVISOR
        return Cipher.to_symbol(i_encoded)

    ### SENDER:
    def encode(self, text: str):
        cipher = ""
        for i in range(len(text)):
            cipher += self.operate_symbol(text[i])
        return cipher

    def corresponding_key(self):
        return (self.DIVISOR - self.key) % self.DIVISOR

    ### RECEIVER:
    def decode(self, text: str):
        return self.encode(text)
