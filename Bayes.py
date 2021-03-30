import os
import sys
import codecs
import math
import numpy as np
from dataHandler import readData
from ngram import getNgrams

def trainBayes():
    regions, name_pairs = readData()
    unigram = getNgrams(1, name_pairs, regions)
    bigram = getNgrams(2, name_pairs, regions)
    trigram = getNgrams(3, name_pairs, regions)

    