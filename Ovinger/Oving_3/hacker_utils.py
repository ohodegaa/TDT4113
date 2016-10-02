__author__ = 'ohodegaa'



class Node:
    def __init__(self):
        self.barn = {}
        self.is_end = False


class WordList:

    def __init__(self, filepath: str = "word_list.txt"):
        self.path = filepath
        self.top_node = Node()
        self.build(self.path)

    def build(self, word_list):
        for word in self.get_word_list():
            node = self.top_node
            i = None
            for i in range(len(word)):
                if node.barn.get(word[i]) is None:
                    node.barn[word[i]] = Node()
                node = node.barn[word[i]]
            if i == len(word) - 1:
                node.is_end = True

    def __contains__(self, text):
        def check_word(word):
            node = self.top_node
            for l in word:
                if node.barn.get(l) is None:
                    return False
                node = node.barn[l]
            return node.is_end

        words = text.split()
        for w in words:
            if not check_word(w.strip()):
                return False

        return True

    def get_word_list(self) -> list:
        return list(open(self.path, "r+").read().splitlines())




def test_timing():
    import time
    print("TIMING:")
    print("Searching for the last word in list ('zyzzyvas')\n")

    start = time.time()
    word_list = WordList()
    print("Build word_tree (open file and generate tree): ", time.time() - start)

    tree = time.time()
    print(word_list.__contains__("zyzzyvas"))
    print("Search tree: ", round(time.time() - tree, 8))

    normal = time.time()
    word_list = open("word_list.txt", "r+").read().splitlines()
    print("Open and read to list: ", time.time() - normal)

    search = time.time()
    print(word_list.__contains__("zyzzyvas"))
    print("Search list: ", time.time() - search)
