#!/usr/bin/python
import os, sys, errno, string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

class GrimReaper(object):

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
        return "".join(c for c in filename if c in valid_chars).encode('utf-8')

    @staticmethod
    def write_to_file(path, filename, data):
        # Recursively create path passed as arg.
        make_path(path)
        data      = data.encode('utf-8')
        full_path = os.path.join(path, filename)

        with open(full_path, "wb") as file_target:
            if type(data) is list:
                for line in data:
                    file_target.write(line + "\n")
            else:
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
    def build_corpus_from_file(path, filename):
        """
        Builds a corpus from a specified file and returns the corpus, which is a
        list of lists of lists. Each sentences is split into its constituent
        series of words.
        Input: pre-processed file.
        Output: list of lists of lists.
        """
        data = GrimReaper.read_from_file(path, filename)
        return [line.split() for line in data]
