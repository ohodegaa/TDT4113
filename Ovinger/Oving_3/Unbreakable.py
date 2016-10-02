__author__ = 'ohodegaa'

from Koder import Cipher
from random import randint


class UnbreakableCipher(Cipher):
    LEGAL_KEYS = open("word_list.txt", "r+").read().splitlines()
    index = 0

    def __init__(self, key: str = None):
        if key is not None:
            self.set_key(key)

    def set_key(self, key):
        self.key = str(key)
        self.index = 0

    def operate_symbol(self, symbol: chr):
        i_text = Cipher.to_index(symbol)
        key = self.key[self.index]
        i_key = Cipher.to_index(key)
        self.index = (self.index + 1) % len(self.key)

        i_generated = (i_text + i_key) % self.DIVISOR
        return Cipher.to_symbol(i_generated)

    ### SENDER:
    def encode(self, text: str):
        cipher = ""
        for i in range(len(text)):
            cipher += self.operate_symbol(text[i])
        return cipher

    ### RECEIVER:
    def decode(self, text: str):
        return self.encode(text)

    @classmethod
    def generate_keys(cls):
        try:
            with open("word_list.txt", "r+") as file:
                words = file.readlines()
        except:
            raise IOError
        word1 = words[randint(0, len(words))].strip()
        word2 = UnbreakableCipher(word1).corresponding_key()

        return word1, word2

    def corresponding_key(self):
        decode_key = ""
        for i in range(len(self.key)):
            i_decode = (self.DIVISOR - Cipher.to_index(self.key[i])) % self.DIVISOR
            decode_key += Cipher.to_symbol(i_decode)
        return decode_key
