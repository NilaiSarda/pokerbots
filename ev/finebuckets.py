"""
==================================================
    Filename:   finebuckets.py

 Description:   Decides later street hand percentiles

     Version:   1.0
     Created:   2017-02-02
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import pickle
import random
import discard
import baseline


def playdiscards(deck, exps, ev):
    """Plays two hands with discards"""
    random.shuffle(deck)
    hole, board = [deck[:2], deck[2:4]], deck[4:7]
    exps[0].append(baseline.evexp(board, hole[0], ev))
    exps[0].append(baseline.evexp(board, hole[1], ev))
    for ind in range(2):
        toss = discard.flop(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[9 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[9 + ind]
    board = deck[4:8]
    exps[1].append(baseline.evexp(board, hole[0], ev))
    exps[1].append(baseline.evexp(board, hole[1], ev))
    for ind in range(2):
        toss = discard.turn(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[11 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[11 + ind]
    board = deck[4:9]
    exps[2].append(baseline.evexp(board, hole[0], ev))
    exps[2].append(baseline.evexp(board, hole[1], ev))


def finebuckets():
    """Fine buckets"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    with open('ev.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    print('starting')
    exps = [[], [], []]
    for _ in range(5 * 10 ** 6):
        playdiscards(deck, exps, ev)
    for ind in range(3):
        exps[ind] = sorted(exps[ind])
        print([exps[ind][len(exps[ind]) * i // 100] for i in range(1, 100)])

finebuckets()
