__author__ = 'ohodegaa'

import re

class File_reader:


    def __init__(self, text):
        self.text = text
        self.word_set = self.generate_word_set()

    def generate_word_set(self):
        word_list = self.text.split(" ")
        word_set = []

        for word in word_list:
            append = True
            word = re.sub('[!"#$%&()=@*.,;:-<>]', '',word)
            word = re.sub('[/]', ' ', word)
            word = word.lower()
            for c in word:
                if c == "'":
                    append = False
                    break
            if append:
                word_set.append(word.strip())

        _2_gram = self.generate_n_grams(word_set, 2)
        _3_gram = self.generate_n_grams(word_set, 3)

        word_set = list(set(word_set))
        return word_set + _2_gram + _3_gram

    def generate_n_grams(self, words, n):
        n_grams = []
        length = len(words)
        for k in range(length - n + 1):
            n_grams.append("_".join(word for word in words[k:k + n]))
        return list(set(n_grams))


    #GETTERS AND SETTERS:
    def get_word_set(self):
        return self.word_set