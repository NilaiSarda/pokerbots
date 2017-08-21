"""
==================================================
    Filename:   evcrunch.py

 Description:   Monte Carlo

     Version:   1.0
     Created:   2017-01-21
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
    hole, board, keys = [deck[:2], deck[2:4]], deck[4:7], [[], []]
    for ind in range(2):
        toss = discard.flop(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[9 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[9 + ind]
    common = tuple(sorted([c[1] for c in board]))
    keys[0].append((common, tuple(sorted([c[1] for c in hole[0]])), baseline.flushcode(board, hole[0])))
    keys[1].append((common, tuple(sorted([c[1] for c in hole[1]])), baseline.flushcode(board, hole[1])))
    board = deck[4:8]
    for ind in range(2):
        toss = discard.turn(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[11 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[11 + ind]
    common = tuple(sorted([c[1] for c in board]))
    common0 = tuple(sorted([c[1] for c in hole[0]]))
    common1 = tuple(sorted([c[1] for c in hole[1]]))
    keys[0].append((common, common0, baseline.flushcode(board, hole[0])))
    keys[1].append((common, common1, baseline.flushcode(board, hole[1])))
    board = deck[4:9]
    common = tuple(sorted([c[1] for c in board]))
    keys[0].append((common, common0, baseline.flushcode(board, hole[0])))
    keys[1].append((common, common1, baseline.flushcode(board, hole[1])))
    return hole, board, keys


def evcrunch():
    """Plays hands on hands on hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    with open('ev.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    print('starting')
    for _ in range(5 * 10 ** 8):
        hole, board, keys = playdiscards(deck)
        hole[0] = [baseline.tostr(c) for c in hole[0]]
        hole[1] = [baseline.tostr(c) for c in hole[1]]
        board = [baseline.tostr(c) for c in board]
        score0 = eval7(board + hole[0])
        score1 = eval7(board + hole[1])  # lower score wins
        for key in keys[0]:
            if key not in ev:
                ev[key] = [0, 0]
            if score0 == score1:
                ev[key][0] += 1
                ev[key][1] += 2
            else:
                if score0 < score1:
                    ev[key][0] += 2
                ev[key][1] += 2
        for key in keys[1]:
            if key not in ev:
                ev[key] = [0, 0]
            if score0 == score1:
                ev[key][0] += 1
                ev[key][1] += 2
            else:
                if score1 < score0:
                    ev[key][0] += 2
                ev[key][1] += 2
    print('finishing')
    with open('ev.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)

evcrunch()
