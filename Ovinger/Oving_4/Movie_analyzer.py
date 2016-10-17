__author__ = 'ohodegaa'

from Folder_handler import Folder_reader
from File_handler import File_reader
from collections import Counter
from operator import itemgetter
import glob
import os
import math


class Analyzer:
    def __init__(self, pos_dir, neg_dir):
        self.pos_dir = Folder_reader(pos_dir)
        self.neg_dir = Folder_reader(neg_dir)
        self.all_dirs = self.merge_dirs(self.pos_dir, self.neg_dir)
        self.prune_all()

    def merge_dirs(self, dir1, dir2):
        dict1 = Counter(dir1.get_counter())
        dict2 = Counter(dir2.get_counter())

        merged_counter = dict1 + dict2
        number_of_files = dir1.get_number_of_files() + dir2.get_number_of_files()

        merged_dir = Folder_reader()
        merged_dir.set_counter(merged_counter)
        merged_dir.set_number_of_files(number_of_files)

        return merged_dir

    def prune_all(self):
        self.prune(self.pos_dir)
        self.prune(self.neg_dir)
        self.prune(self.all_dirs)


    def get_most_popular_words(self, dir: Folder_reader):
        num_of_files = dir.get_number_of_files()
        counter = dir.get_counter()

        def get_key(item):
            nonlocal num_of_files
            return item[1] / num_of_files

        return [[word[0], get_key(word)] for word in sorted(counter.items(), reverse=True, key=get_key)[0:25]]

    def get_propability(self, words, num_of_files):
        for word in words:
            word[1] = round(word[1] / num_of_files, 4)
        return words

    def get_informative_value(self, dir: Folder_reader):
        counter = dir.get_counter()
        all_counter = self.all_dirs.get_counter()

        def get_key(item):
            nonlocal all_counter
            return item[1]/all_counter.get(item[0])

        return dict((word[0], get_key(word)) for word in sorted(counter.items(), reverse=True, key=get_key)[0:34])

    def prune(self, dir):
        [dir.get_counter().pop(key) for key in [k if ((v/self.all_dirs.get_number_of_files()) < 0.03 or any(c in Folder_reader.stop_words for c in k.split("_"))) else "" for k, v in dir.get_counter().items()] if key in dir.get_counter().keys()]


    def classification(self, pos_dir, neg_dir):
        neg_counter = self.get_informative_value(self.neg_dir)
        pos_counter = self.get_informative_value(self.pos_dir)

        good_movies = []
        bad_movies = []

        correct = True

        for dir in [pos_dir, neg_dir]:
            for file in glob.glob(os.path.join(dir, '*.txt')):
                word_set = File_reader(open(file, encoding='utf-8').read()).get_word_set()

                pos_val = self.get_pos_value(word_set, neg_counter, pos_counter)
                neg_val = self.get_neg_value(word_set, neg_counter, pos_counter)

                if pos_val > neg_val:
                    good_movies.append((file, correct))
                else:
                    bad_movies.append((file, not correct))

            correct = not correct

        return good_movies, bad_movies

    def get_movie_value(self, word_set, neg_counter: dict, pos_counter: dict, i):
        value = 0.0

        for word in word_set:
            if (word not in neg_counter.keys()) and (word not in pos_counter.keys()):
                continue

            if word in pos_counter.keys():
                value -= i*math.log10(float(pos_counter.get(word)))

            if word in neg_counter.keys():
                value += i*math.log10(float(neg_counter.get(word)))

        return value

    def get_pos_value(self, word_set, neg_counter: dict, pos_counter: dict):
        return self.get_movie_value(word_set, neg_counter, pos_counter, 1)

    def get_neg_value(self, word_set, neg_counter: dict, pos_counter: dict):
        return self.get_movie_value(word_set, neg_counter, pos_counter, -1)

    def evaluate(self, pos_dir, neg_dir):
        good_movies, bad_movies = self.classification(pos_dir, neg_dir)
        num_of_files = len([file for file in os.listdir(pos_dir)]) + len([file for file in os.listdir(neg_dir)])

        correct_guesses = 0

        for movie in good_movies:
            if movie[1]:
                correct_guesses += 1

        for movie in bad_movies:
            if movie[1]:
                correct_guesses += 1
        return correct_guesses / num_of_files


train_pos_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/subset/train/pos"
train_neg_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/subset/train/neg"

test_pos_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/subset/test/pos"
test_neg_path = "/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/subset/test/neg"

analyzer = Analyzer(train_pos_path, train_neg_path)

print(analyzer.evaluate(test_pos_path, test_neg_path))
print(analyzer.get_most_popular_words(analyzer.pos_dir))
print(analyzer.get_informative_value(analyzer.pos_dir))
