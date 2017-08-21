"""
==================================================
    Filename:   preflopbuckets.py

 Description:   Explicitly solves preflop

     Version:   1.0
     Created:   2017-01-28
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import pickle
import itertools
import baseline


def preflopbuckets():
    """Preflopbuckets"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    with open('preflopev.pickle', 'rb') as handle:
        preflop = pickle.load(handle)
    edge = []
    for hole in itertools.combinations(deck, 2):
        edge.append((baseline.preflopexp(hole, preflop), sorted(hole)))
    edge = tuple([h[1] for h in sorted(edge)])
    with open('edge.pickle', 'wb') as handle:
        pickle.dump(edge, handle, protocol=2)

preflopbuckets()
