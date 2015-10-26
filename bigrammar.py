#!/usr/bin/python

from __future__ import division
import random, math
from operator import itemgetter
from collections import defaultdict
from GrimReaper import *

# Constants
FILE_NAME = "movies.txt"

class BigramModel(object):
    """
    Unsmoothed Bigram Language model.
    """
    def __init__(self, corpus):
        self.bigram_dist = BigramDist(corpus)

    def generate_number_suffix(self):
        return "\t" + str(random.randint(0, 242))

    def generate_bigram(self):
        return self.bigram_dist.draw_bigram()

    def generate_bigram_with_suffix(self):
        return self.bigram_dist.draw_bigram() + str(self.generate_number_suffix())

# Class for a unsmoothed bigram probability distribution
class BigramDist:
    def __init__(self, corpus):
        self.counts      = defaultdict(lambda: defaultdict(float))
        self.prev_counts = defaultdict(float)
        self.prev_length = 0.0
        self.train(corpus)

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            prev_word = sen[0]
            self.prev_counts[prev_word] += 1.0

            for word in sen[1:]:
                self.counts[prev_word][word] += 1.0
                self.prev_counts[word]       += 1.0
                prev_word = word

        self.prev_length = len(self.prev_counts)
        print "Done training."

    # Returns the probability of word in the distribution
    def prob(self, word, given):
        return self.counts[given][word] / self.prev_counts[given]

    def draw_start(self):
        return self.prev_counts.keys()[random.randint(0, self.prev_length - 1)]

    # Generate a single random word according to the distribution
    def draw(self, prev):
        ret = END_SYMBOL
        if prev != None:
            rand = random.random()
            for word in self.counts[prev].keys():
                p = self.prob(word, prev)
                rand -= p
                if rand <= 0.0:
                    ret = word
        if ret == END_SYMBOL:
            ret = self.draw_start()

        return ret

    def draw_bigram(self):
        prev = self.draw_start()
        return prev + " " + self.draw(prev)

if __name__ == "__main__":
    random.seed(0)
    corpus = GrimReaper.build_corpus_from_file("", FILE_NAME)
    bigram = BigramModel(corpus)
    B = 1024
    KB = B*B
    MB = KB*B
    GB = MB*B
    file_size = 70*MB
    output_name = "gabby.txt"
    interval = MB
    # Ain't no do while in python
    GrimReaper.write_to_file("data", output_name, [bigram.generate_bigram_with_suffix() for i in xrange(interval)])
    while GrimReaper.get_file_size("data", output_name)*B < file_size:
        print GrimReaper.get_file_size("data", output_name)
        GrimReaper.write_to_file("data", output_name, [bigram.generate_bigram_with_suffix() for i in xrange(interval)])
        print "Onto the next one..."
