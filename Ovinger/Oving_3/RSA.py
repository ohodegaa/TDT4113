__author__ = 'ohodegaa'

import Koder
from crypto_utils import generate_random_prime as randp
from random import randint
import crypto_utils as cu


class RSACipher(Koder.Cipher):
    LEGAL_KEYS = range(8, 257)

    def __init__(self, no_bits, n=None, e=None):
        super(RSACipher, self).__init__()
        self.d = None
        self.n = n
        self.e = e

        self.no_bits = int(no_bits)
        if n is None and e is None:
            self.generate_encryption()

    def generate_encryption(self):

        while self.d is None:
            p = 0
            q = 0
            while p == q:
                p = randp(self.no_bits)
                q = randp(self.no_bits)
            self.n = p * q
            phi = (p - 1) * (q - 1)
            self.e = randint(3, phi - 1)
            self.d = cu.modular_inverse(self.e, phi)

    def get_encryption(self):
        return self.n, self.e

    def encode(self, text: str) -> str:

        def encode_number(number: int) -> str:
            return str(pow(number, self.e, self.n))

        def encode_text(text: str) -> str:
            blocks = cu.blocks_from_text(text, 4)
            cipher = ""
            for block in blocks:
                cipher += str(encode_number(block)) + " "
            return cipher

        try:
            number = int(text)
            return str(encode_number(number))
        except ValueError:
            return str(encode_text(text))

    def decode(self, text: str):
        def decode_number(number: int) -> int:
            return pow(number, self.d, self.n)

        def decode_text(text: str):
            blocks = text.split()
            decrypted = []
            for block in blocks:
                decrypted.append(decode_number(int(block)))
            return cu.text_from_blocks(decrypted, self.no_bits)

        return decode_text(text)

    def verify(self, text: str, sender: Koder = None, receiver: Koder = None):

        print("Verifying for class RSACipher begins...")
        print("Input text:\n", text, "\n")
        print("Encoding...\n")
        test_cipher = sender.encode(text)
        print("Decoding...\n")
        test_plain_text = receiver.decode(test_cipher)
        print("After decoding:\n", test_plain_text, "\n")

        for i in range(len(test_plain_text)):
            if test_plain_text[i] != text[i]:
                return False
        return True

    def corresponding_key(self):
        pass

    def generate_keys(self):
        pass

    def operate_symbol(self, symbol: chr):
        pass
