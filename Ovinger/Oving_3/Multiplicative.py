__author__ = 'ohodegaa'

from Koder import Cipher
import crypto_utils as cu


class MultiplicativeCipher(Cipher):

    def __init__(self, key: int = None):
        if key is not None:
            self.set_key(key)

    def set_key(self, key):
        self.key = int(key)

    def operate_symbol(self, symbol: chr):
        i = Cipher.to_index(symbol)
        i_encoded = (i * self.key) % self.DIVISOR
        return Cipher.to_symbol(i_encoded)

    ### SENDER:
    def encode(self, text: str):
        cipher = ""
        for i in range(len(text)):
            cipher += self.operate_symbol(text[i])
        return cipher

    def corresponding_key(self):
        mod_inverse = None
        while mod_inverse is None:
            mod_inverse = cu.modular_inverse(self.key, self.DIVISOR)
            if mod_inverse is None:
                print("A modular inverse is not found, please choose a different key")
                self.key = int(input("Key: "))
        return mod_inverse

    ### RECEIVER:
    def decode(self, text: str):
        return self.encode(text)
