__author__ = 'ohodegaa'

from Koder import Cipher
from Affine import AffineCipher
from Caesar import CaesarCipher
from Multiplicative import MultiplicativeCipher
from Unbreakable import UnbreakableCipher
from RSA import RSACipher

from abc import ABCMeta


class Person(metaclass=ABCMeta):
    LEGAL_CIPHERS = ["Caesar", "Multiplicative", "Unbreakable", "Affine", "RSA"]

    LEGAL_AFFINE_KEYS = "TWO positive numbers, separated by ','"
    LEGAL_RSA_RANGE = "From 8 to 256"
    LEGAL_KEYS = ["All positive numbers, from 1 to 94",
                  "All positive numbers, from 0 to 1 000 000"]
    LEGAL_UNBREAKABLE_KEYS = "An english word"

    key = None

    cipher = None

    def __init__(self, cipher: Cipher = None):
        if not issubclass(type(cipher), Cipher) and cipher is not None:
            raise TypeError
        self.cipher = cipher

    def set_key(self, key: str):
        """
        Sets the key for the preferred cipher
        :param key: the key
        :return: True if key is valid? else False???
        """
        self.key = key

    def get_key(self):
        """
        Returns the key
        :return: self.key
        """
        return self.key


class Sender(Person):
    encoded_text = ""

    def encode(self, text: str):
        """
        Encodes a text and returns a ciphered text
        :param text: the text to be encoded
        :return: the encoded text
        """
        self.encoded_text = self.cipher.encode(text)

    def get_encoded_text(self):
        return self.encoded_text


class Receiver(Person):
    decoded_text = ""

    def decode(self, text: str):
        """
        Decodes a ciphered text and returns a text
        :param text: the text to be decoded
        :return: the decoded text
        """
        self.decoded_text = self.cipher.decode(text)

    def get_decoded_text(self):
        return self.decoded_text


def main():
    cipher = ask_for_cipher()
    key = ask_for_key(cipher)

    if cipher == "RSA":
        receiver_cipher = eval(cipher + "Cipher('" + str(key) + "')")
        n, e = receiver_cipher.get_encryption()
        sender_cipher = RSACipher(key, n, e)

    else:
        sender_cipher = eval(cipher + "Cipher('" + str(key) + "')")

        receiver_cipher = eval(cipher + "Cipher(" + '"' + str(sender_cipher.corresponding_key()) + '"' + ")")

    sender = Sender(sender_cipher)
    receiver = Receiver(receiver_cipher)

    while True:
        text = input("Sender message: 'q' for exit")
        if text == 'q':
            break
        sender.encode(text)
        encoded_text = sender.get_encoded_text()
        print("Encoded text:        " + encoded_text)

        receiver.decode(encoded_text)
        decoded_text = receiver.get_decoded_text()
        print("Decoded text:        " + decoded_text)


def ask_for_key(cipher):
    if cipher == "RSA":
        no_bits = 0
        print("Choose how many bits your RSA-cipher should contain")
        print("Legal range:\n", Person.LEGAL_RSA_RANGE)
        while True:
            no_bits = int(input(">>>"))
            if no_bits in RSACipher.LEGAL_KEYS:
                break
            else:
                print("Not in legal range, please try again")

        return no_bits

    elif cipher == "Affine":
        keys = None
        print("Choose keys for Affine-cipher")
        print("Legal range:\n", Person.LEGAL_AFFINE_KEYS)
        while True:
            keys = input(">>>")
            keys = keys.split(',')
            if int(keys[0]) in Cipher.LEGAL_KEYS and int(keys[1]) in Cipher.LEGAL_KEYS:
                break
            else:
                print("This is not legal keys, please try again")

        return int(keys[0]), int(keys[1])

    elif cipher == "Unbreakable":
        key = None
        print("Choose keys for Unbreakable-cipher")
        print("Legal range:\n", Person.LEGAL_UNBREAKABLE_KEYS)
        while True:
            key = input(">>>")
            for ch in key:
                if ch not in Cipher.LEGAL_SYMBOLS:
                    print("This is not a legal key, please try again")
                    continue
            break

        return key

    else:
        key = None
        print("Choose key:")
        print("Legal keys:\n", Person.LEGAL_KEYS[Person.LEGAL_CIPHERS.index(cipher)])
        while True:
            key = int(input(">>>"))
            if key in eval(cipher + "Cipher").LEGAL_KEYS:
                break
            else:
                print("This is not a legal key, please try again")

        return key


def ask_for_cipher():
    cipher = None
    print("Choose cipher: ")
    print("Ciphers available:")
    for a in Person.LEGAL_CIPHERS:
        print(" - " + a)

    while True:
        cipher = input(">>>")
        if cipher in Person.LEGAL_CIPHERS:
            break
        else:
            print("This is not a chiper, please try again")

    return cipher


if __name__ == '__main__':
    main()
