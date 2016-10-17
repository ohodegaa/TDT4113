__author__ = 'ohodegaa'

import glob
import re

class File_reader():

    n = [2,3]
    dir_path = ""
    stop_words_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/stop_words.txt"
    num_pos_reviews = None
    num_neg_reviews = None
    legal_chars = [chr(j) for j in range(ord('a'), ord('z') + 1)] + [chr(j) for j in range(ord('0'), ord('9') + 1)] + ['_', '/']

    def __init__(self, dir_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/subset"):
        self.dir_path = dir_path
        self.stop_words = open(self.stop_words_path).read().split()


    def read_test(self):
        """
        :return: (neg_files, pos_files) where neg_files/pos_files is lists of the files with neg/pos reviews
        """
        path = self.dir_path + "/test"
        neg_path = path + "/neg"
        pos_path = path + "/pos"

        neg_files = glob.glob(neg_path + '/*.txt')
        pos_files = glob.glob(pos_path + '/*.txt')
        self.num_neg_reviews = len(neg_files)
        self.num_pos_reviews = len(pos_files)

        return neg_files, pos_files


    def get_list_of_reviews(self):
        neg_files, pos_files = self.read_test()

        result = [[], []]
        for i in range(len([neg_files, pos_files])):  # neg, pos
            reviews = []
            for j in range(len([neg_files, pos_files][i])):  # each file in neg or pos
                words = []
                for line in open([neg_files, pos_files][i][j]):
                    for word in line.split():
                        if not any(c == "'" for c in word):
                            word = word.lower()
                            word = re.sub('[!"#$%&()=@*.,;:-<>]', '', word)
                            word = re.sub('[\/]', ' ', word)
                            word = word.strip()
                            if not self.is_stop_word(word) and len(word) > 1:
                                words.append(word)
                self.add_n_grams(words)
                reviews.append(words)
            result[i] = reviews
        return result[0], result[1]

    def get_total_revs_count(self):
        return self.num_neg_reviews + self.num_pos_reviews

    def get_pos_revs_count(self):
        return self.num_pos_reviews

    def get_neg_revs_count(self):
        return self.num_neg_reviews

    def get_revs_count(self, pos_or_neg):
        if pos_or_neg:
            return self.get_pos_revs_count()
        else:
            return self.get_neg_revs_count()


    def add_n_grams(self, words):
        for n in self.n:
            length = len(words)
            for k in range(length - n + 1):
                words.append("_".join(word for word in words[k:k + n]))

    def is_stop_word(self, word):
        return word in self.stop_words


class Analyze_data:


    def __init__(self):
        self.negative_counter = None
        self.positive_counter = None
        self.positive_revs = None
        self.negative_revs = None
        self.all_reviews = None

        self.reader = File_reader()
        neg, pos = self.reader.get_list_of_reviews()
        self.update(neg, pos)

        self.total_counter = self.word_counter_total(self.negative_revs, self.positive_revs)


    def update_reviews(self, neg_revs, pos_revs):
        self.negative_revs, self.positive_revs = neg_revs, pos_revs
        self.all_reviews = self.negative_revs + self.positive_revs

    def update_word_counter(self):
        self.negative_counter = self.word_counter(self.negative_revs)
        self.positive_counter = self.word_counter(self.positive_revs)
        self.total_counter = self.word_counter_total(self.negative_revs, self.positive_revs)

    def update(self, neg_revs, pos_revs):
        self.update_reviews(neg_revs, pos_revs)
        self.update_word_counter()


    def word_counter(self, reviews) -> dict:
        """
        :param reviews: list, either positive or negative, of lists of words in a review
        :return: a dictionary with key: word, value: how many reviews 'word' is mentioned in
        """
        words = {}
        for review in reviews:
            rev = []
            for w in review:
                if w.strip() not in rev:
                    rev.append(w.strip())
                    if words.get(w) is not None:
                        words[w] += 1
                    else:
                        words[w] = 1
        return words


    def word_counter_total(self, neg_rev, pos_rev):
        """

        :param neg_rev: a list of lists of words in each negative review
        :param pos_rev: a list of lists of words in each positive review
        :return: a dictionary containing all words from all reviews (pos and neg) with corresponding word count as value
        """
        words = {}
        for reviews in [neg_rev, pos_rev]:
            for review in reviews:
                rev = []
                for w in review:
                    if w.strip() not in rev:
                        rev.append(w.strip())
                        if words.get(w) is not None:
                            words[w] += 1
                        else:
                            words[w] = 1
        return words


    def get_most_informative_words(self, pos_or_neg):
        def getKey(item):
            return item[1]
        most_informative_words = []
        word_counter = self.get_word_counter(pos_or_neg)

        for k, v in word_counter.items():
            most_informative_words.append((k, (v/self.total_counter.get(k))))

        return sorted(most_informative_words, reverse=True, key=getKey)[:25]


    def pruning(self):
        words_to_prune = []

        for


    def get_reviews(self, pos_or_neg):
        if pos_or_neg:
            return self.positive_revs
        else:
            return self.negative_revs

    def get_word_counter(self, pos_or_neg):
        if pos_or_neg:
            word_counter = self.positive_counter
        else:
            word_counter = self.negative_counter

        return word_counter

        

    def get_most_popular_words(self, reviews):
        def get_key(item):
            return item[1]
        word_count = self.word_counter(reviews)
        most_popular_words = sorted(word_count.items(), reverse=True, key=get_key)
        return most_popular_words



def main():
    analyzer = Analyze_data()





if __name__ == '__main__':
    main()