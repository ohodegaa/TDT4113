__author__ = 'ohodegaa'

import hacker_utils as util
from abc import ABCMeta
from Koder import Cipher
from crypto_utils import modular_inverse as modin
import time

class Hacker(metaclass=ABCMeta):
    print("Setting up hacker...\n\n")
    start_time = time.time()
    word_list = util.WordList("word_list.txt")
    print("Word list ready for hacking procedure...\n\n")
    print("-" * 45)

    def __init__(self):
        self.possible_words = {}

    def hack_all(self, text):
        hackers = [CaesarHacker(), MultiplicativeHacker(), AffineHacker(), UnbreakableHacker()]
        for hacker in hackers:
            print("Testing with " + hacker.__class__.__name__)

            hacker.hack(text)
            print("Results from " + hacker.__class__.__name__ + ":   " + str(len(hacker.possible_words)))
            counter = 1
            for possible_word in hacker.possible_words.keys():
                print("     " + str(counter) + ".")
                counter += 1
                print("     Secret message:    ", possible_word)
                print("     Encode key:      ", hacker.possible_words[possible_word][0])
                print("     Decode key:      ", hacker.possible_words[possible_word][1])
            print("\n\n")
            print("-" * 45)

        print("Hacking completed in", time.time() - self.start_time, "seconds. Please review results above!")


    def hack(self, word):
        pass


class CaesarHacker(Hacker):
    def hack(self, word):
        from Caesar import CaesarCipher
        hacker = CaesarCipher()
        for encode_key in hacker.LEGAL_KEYS:
            hacker.set_key(encode_key)
            decode_key = hacker.corresponding_key()
            hacker.set_key(decode_key)
            decoded_text = hacker.decode(word)
            if self.word_list.__contains__(decoded_text):
                self.possible_words[decoded_text] = (encode_key, decode_key)


class MultiplicativeHacker(Hacker):
    def hack(self, word):
        from Multiplicative import MultiplicativeCipher
        hacker = MultiplicativeCipher()
        for encode_key in hacker.LEGAL_KEYS:
            if modin(encode_key, Cipher.DIVISOR) is not None:
                hacker.set_key(encode_key)
                decode_key = hacker.corresponding_key()
                hacker.set_key(decode_key)
                decoded_text = hacker.decode(word)
                if self.word_list.__contains__(decoded_text):
                    self.possible_words[decoded_text] = (encode_key, decode_key)


class AffineHacker(Hacker):
    def hack(self, word):

        from Affine import AffineCipher
        hacker = AffineCipher()
        for encode_key1 in hacker.LEGAL_KEYS:
            if modin(encode_key1, Cipher.DIVISOR) is not None:
                for encode_key2 in hacker.LEGAL_KEYS:
                    hacker.set_key((encode_key1, encode_key2))
                    decode_key = hacker.corresponding_key()
                    hacker.set_key(decode_key)
                    decoded_text = hacker.decode(word)
                    if self.word_list.__contains__(decoded_text):
                        self.possible_words[decoded_text] = ((encode_key1, encode_key2), decode_key)


class UnbreakableHacker(Hacker):
    def hack(self, word):
        from Unbreakable import UnbreakableCipher
        hacker = UnbreakableCipher()
        for encode_key in hacker.LEGAL_KEYS:
            hacker.set_key(encode_key)
            decode_key = hacker.corresponding_key()
            hacker.set_key(decode_key)
            decoded_text = hacker.decode(word)
            if self.word_list.__contains__(decoded_text):
                self.possible_words[decoded_text] = (encode_key, decode_key)


def main():
    hacker = Hacker()
    hacker.hack_all(r"YOggQpWtzPRW`zKdijgFpNjb")


if __name__ == '__main__':
    main()
