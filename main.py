#!/usr/bin/python

import bigrammar
from filey import *

data = GrimReaper.build_corpus_from_file("", "movies.txt")

for line in data:
    print line
