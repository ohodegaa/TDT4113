__author__ = 'ohodegaa'

import crypto_utils as cu
from random import randint
from abc import abstractclassmethod, abstractmethod, ABCMeta


class Cipher(metaclass=ABCMeta):
    LEGAL_SYMBOLS = [chr(i) for i in range(32, 127)]
    LEGAL_KEYS = range(0, len(LEGAL_SYMBOLS))
    DIVISOR = len(LEGAL_SYMBOLS)
    key = None

    ### CLASS METHODS:
    @classmethod
    def to_index(cls, ascii_symbol: chr):

        """
        Converts an ascii chr to the index in LEGAL_SYMBOLS
        :param ascii_symbol: symbol to convert to index
        :return: index of symbol
        """
        return cls.LEGAL_SYMBOLS.index(ascii_symbol)

    @classmethod
    def to_symbol(cls, index: int):
        """
        Converts from index (relative to LEGAL_SYMBOLS) to
        ascii symbol
        :param index: index to convert
        :return: ascii chr corresponding to the index
        """
        return cls.LEGAL_SYMBOLS[index]

    @classmethod
    def generate_keys(cls):
        """
        Generates a tuple with keys which to be distributed
        to sender and/or receiver
        :return: tuple  (key1, key2)
        """
        key2 = None
        while key2 is None:
            key1 = randint(0, cls.DIVISOR)
            key2 = cu.modular_inverse(key1, cls.DIVISOR)
        return key1, key2

    ### SENDER ONLY METHODS:
    @abstractmethod
    def encode(self, text: str) -> str:
        """
        Encodes the text using a key
        :param text: the text to be encoded into cipher text
        :return: the encoded text
        """
        pass

    @abstractmethod
    def corresponding_key(self):
        pass

    ### RECEIVER ONLY METHODS:
    @abstractmethod
    def decode(self, text: str) -> str:
        """
        Decodes the ciphered text received using a valid key
        :param text: the ciphered text to be decoded
        :return: the decoded text
        """
        pass

    ### SENDER AND RECEIVER METHODS:
    @abstractmethod
    def operate_symbol(self, symbol: chr):
        """
        Converts a symbol with the wanted implementation
        :param symbol: the symbol which to convert
        :return: the converted symbol
        """
        pass
    @staticmethod
    def verify(text: str, sender, receiver):
        """
        Verifies if the encoding-decoding ciphers correct.
        Will first do an encoding and then a decoding, before
        comparing the text to the original
        :param text: input text to be verified
        :param sender: used in RSACipher's verify()-method
        :param receiver: used in RSACipher's verify()-method
        :return:
            True, if it encodes/decodes correctly
            False, if it encodes/decodes incorrectly
        """

        test_cipher = sender.encode(text)
        test_plain_text = receiver.decode(test_cipher)
        print("encoded text: ", test_cipher)
        print("decoded text: ", test_plain_text)

        for i in range(len(test_cipher)):
            if test_plain_text[i] != text[i]:
                return False
        return True


    ###HACKER METHODS:
    def set_key(self, key):

        self.key = key