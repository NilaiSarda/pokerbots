"""
==================================================
    Filename:   preflopcrunch.py

 Description:   Monte Carlo

     Version:   1.0
     Created:   2017-01-25
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
from poker import eval7
import discard
import baseline


def playdiscards(deck):
    """Plays two hands with discards"""
    random.shuffle(deck)
    hole, board = [deck[:2], deck[2:4]], deck[4:7]
    keys = [baseline.preflopkeygen(hole[0]), baseline.preflopkeygen(hole[1])]
    for ind in range(2):
        toss = discard.flop(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[9 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[9 + ind]
    board = deck[4:8]
    for ind in range(2):
        toss = discard.turn(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[11 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[11 + ind]
    board = deck[4:9]
    return hole, board, keys


def preflopcrunch():
    """Plays hands on hands on hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    with open('preflop.pickle', 'rb') as handle:
        preflop = pickle.load(handle)
    for _ in range(5 * 10 ** 6):
        hole, board, keys = playdiscards(deck)
        hole[0] = [baseline.tostr(c) for c in hole[0]]
        hole[1] = [baseline.tostr(c) for c in hole[1]]
        board = [baseline.tostr(c) for c in board]
        score = [eval7(board + hole[0]), eval7(board + hole[1])]
        if keys[0] not in preflop:
            preflop[keys[0]] = [0, 0]
        if score[0] == score[1]:
            preflop[keys[0]][0] += 1
            preflop[keys[0]][1] += 2
        else:
            if score[0] < score[1]:
                preflop[keys[0]][0] += 2
            preflop[keys[0]][1] += 2
        if keys[1] not in preflop:
            preflop[keys[1]] = [0, 0]
        if score[0] == score[1]:
            preflop[keys[1]][0] += 1
            preflop[keys[1]][1] += 2
        else:
            if score[1] < score[0]:
                preflop[keys[1]][0] += 2
            preflop[keys[1]][1] += 2
    with open('preflop.pickle', 'wb') as handle:
        pickle.dump(preflop, handle, protocol=2)

preflopcrunch()
