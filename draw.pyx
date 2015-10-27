#import random
from libc.stdlib cimport rand

# TODO: This is probably the wrong way to generate random numbers
# in cython:
# http://stackoverflow.com/questions/16138090/correct-way-to-generate-random-numbers-in-cython
def cdraw(counts, prob, str prev):
    """
    TODO: Figure out how to actually use strings in cython...
    http://docs.cython.org/src/tutorial/strings.html

    TODO: This solution is so jank. You might as well replace it
    with the kosher scipy function.

    Parameters
    ----------
    counts : Dictionary
        Counts for words, given prev as a prior. (Prev has already
        been determined.)
    """
    cdef str ret = "</s>"
    cdef float rand_num = rand()
    cdef float p = 0
    for word in counts.iterkeys():
        p = prob(word, prev)
        rand_num -= p
        if rand_num <= 0.0:
            ret = word
            break
    return ret
