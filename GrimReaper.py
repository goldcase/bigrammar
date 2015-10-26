#!/usr/bin/python
import os, sys, errno, string

#Constants
VALID_CHARS   = "%s%s" % (string.ascii_letters, string.digits)
INVALID_ELEMS = list(string.punctuation)
START_SYMBOL  = "<s>"
END_SYMBOL    = "</s>"

class GrimReaper(object):
    """
    GrimReaper is master of your corpus.
    """

    # Tries to make path and only catches exceptions not relating to directory
    # already existing.
    @staticmethod
    def make_path(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def already_exists(path, filename):
        full_path = os.path.join(path, filename)
        return os.path.exists(full_path)

    @staticmethod
    def scrub_file_name(filename):
        return "".join(c for c in filename if c in VALID_CHARS).encode('utf-8')

    @staticmethod
    def write_to_file(path, filename, data):
        # Recursively create path passed as arg.
        GrimReaper.make_path(path)
        full_path = os.path.join(path, filename)

        with open(full_path, "ab") as file_target:
            if type(data) is list:
                for line in data:
                    line = line.encode('utf-8')
                    file_target.write(line + "\n")
            else:
                data = data.encode('utf-8')
                file_target.write(data)

    @staticmethod
    def read_from_file(path, filename):
        """
        Reads in a file and outputs an array of each read-in line.
        Input: path, filename
        Output: list of lists
        """
        with open(os.path.join(path, filename), "r") as file_source:
            data = [line.rstrip("\n") for line in file_source]

        return data

    @staticmethod
    def preprocess_corpus(corpus):
        """
        Remove invalid elems (like punctuation) from the corpus.
        """
        ret = []
        for sen in corpus:
            temp = [x for x in sen if x not in INVALID_ELEMS]
            if not temp:
                continue
            temp.append(END_SYMBOL)
            ret.append(temp)

        return ret

    @staticmethod
    def build_corpus_from_file(path, filename):
        """
        Builds a corpus from a specified file and returns the corpus, which is a
        list of lists. Each sentences is split into its constituent
        series of words.
        Input: pre-processed file.
        Output: list of lists.
        """
        data = GrimReaper.read_from_file(path, filename)
        corpus = [line.split() for line in data]
        return GrimReaper.preprocess_corpus(corpus)
