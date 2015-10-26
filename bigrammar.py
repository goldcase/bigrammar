#!/usr/bin/python

from __future__ import division
import random, math
from operator import itemgetter
from collections import defaultdict
from GrimReaper import *

# Constants
FILE_NAME    = "movies.txt"

# Unsmoothed bigram language model
class BigramModel(object):
    def __init__(self, corpus):
        self.bigramDist = BigramDist(corpus)

    def generate_sentence(self):
        sen = []
        sen.append(START_SYMBOL)

        while sen[-1] != END_SYMBOL:
            drawn = self.bigramDist.draw(sen[-1])
            if drawn != START_SYMBOL:
                sen.append(drawn)

        return sen

    def generate_sentence_with_number(self):
        sen = self.generate_sentence()
        return sen + "\t" + str(random.randInt())

    def get_sentence_probability(self, sen):
        prob = 1.
        prev = ""
        for word in sen:
            if word != START_SYMBOL:
                prob *= self.bigramDist.prob(word, prev)
            prev = word

        return prob

    def get_corpus_perplexity(self, corpus):
        corpus_length = 0
        log_total     = 0

        for sen in corpus:
            prev = sen[0]
            for word in sen[1:]:
                corpus_length += 1
                p = self.bigramDist.prob(word, prev)
                if p != 0:
                    log_total += math.log(p)
                else:
                    return float('Inf')
                prev = word

        return math.exp(-log_total/corpus_length)

# Class for a unsmoothed bigram probability distribution
class BigramDist:
    def __init__(self, corpus):
        self.counts = defaultdict(lambda: defaultdict(float))
        self.total = defaultdict(float)
        self.train(corpus)

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            prev_word = sen[0]
            self.total[prev_word] += 1.0
            for word in sen[1:]:
                self.counts[prev_word][word] += 1.0
                self.total[word] += 1.0
                prev_word = word

    # Returns the probability of word in the distribution
    def prob(self, word, given):
        ret = self.counts[given][word] / self.total[given]
        return ret

    # Generate a single random word according to the distribution
    def draw(self, prev):
        if prev != None:
            rand = random.random()

            for word in self.counts[prev].keys():
                p = self.prob(word, prev)
                rand -= p
                if rand <= 0.0:
                    return word

if __name__ == "__main__":
    corpus = GrimReaper.build_corpus_from_file("", FILE_NAME)
    bigram = BigramModel(corpus)
    print bigram.generate_sentence()
