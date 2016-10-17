__author__ = 'ohodegaa'

from File_handler import File_reader

import os
import glob


class Folder_reader:
    stop_words = open("/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/stop_words.txt", encoding='utf-8').read().split()

    def __init__(self, folder="/Users/olehakon95/Documents/OneDrive - NTNU/Arstrinn_2/semester_3_host/ProgLAB/Ovinger/Oving_4/data/default"):
        self.word_counter = self.generate_counter(folder)
        self.number_of_files = len(os.listdir(folder))


    def generate_counter(self, folder):
        word_counter = {}

        for file in glob.glob(os.path.join(folder, '*.txt')):
            word_set = File_reader(open(file, encoding='utf-8').read()).get_word_set()
            for word in word_set:
                if word not in word_counter.keys() and word not in Folder_reader.stop_words:
                    word_counter[word] = 1
                elif word not in Folder_reader.stop_words:
                    word_counter[word] += 1

        return word_counter


    # GETTERS AND SETTERS:
    def get_counter(self):
        return self.word_counter

    def set_counter(self, counter):
        self.word_counter = counter

    def get_number_of_files(self):
        return self.number_of_files

    def set_number_of_files(self, number):
        self.number_of_files = number




