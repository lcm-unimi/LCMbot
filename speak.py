# -*- coding: utf-8 -*-
import numpy as np
from sys import argv
from random import random as rand


def produce_sentence(word=None):
    # load beginnigs, ends, and pairs of words
    begs = np.loadtxt('words_db/beginnings', dtype=[('w','S20'), ('p','f8')])
    ends = np.loadtxt('words_db/ends', usecols=(0,), dtype=str)
    pairs = np.loadtxt('words_db/pairs',
                       dtype=[('w1', 'S20'), ('w2', 'S20'), ('p','f8')])

    # normalise probabilities
    begs['p'] /= begs['p'].sum()

    if word is not None:
        word = str(word) # dark ritual to fix issue with re-encoding unicode
        sentence = [word]
        if word not in begs['w'] and word not in pairs['w2']:
            sentence = (['We', 'never', 'said', word + '.'])
            word = np.random.choice(begs['w'], p=begs['p'])
        else:
            # build sentence backwards from word to beginning
            # 1 out of 4 times try to go backwards even if word is a beginning
            while sentence[0] not in begs['w'] \
                    or (rand() < 0.25 and sentence[0] in pairs['w2']):
                tmp_pairs = pairs[pairs['w2'] == sentence[0]]
                norm_probs = tmp_pairs['p'] / tmp_pairs['p'].sum()
                sentence.insert(0, np.random.choice(tmp_pairs['w1'],
                                p=norm_probs))
    else:
        # choose a beginning and start sentence
        word = np.random.choice(begs['w'], p=begs['p'])
        sentence = [word]

    # create rest of the sentence
    # if sentence reaches 15 words length, just stop
    while len(sentence) < 15 or word not in ends:
        while word not in pairs['w1']:
            # cannot continue from here. let's start again
            sentence[-1] += '.'
            word = np.random.choice(begs['w'], p=begs['p'])
            sentence.append(word)

        # add word to sentence
        tmp_pairs = pairs[pairs['w1'] == word]
        norm_probs = tmp_pairs['p'] / tmp_pairs['p'].sum()
        word = np.random.choice(tmp_pairs['w2'], p=norm_probs)
        sentence.append(word)

    return ' '.join(sentence) + '.'


if __name__ == "__main__":
    print produce_sentence(argv[1] if len(argv) > 1 else None)
