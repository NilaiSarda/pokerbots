"""
==================================================
    Filename:   buckets.py

 Description:   Splits up hands evenly into buckets by ev

     Version:   1.0
     Created:   2017-01-26
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


def playdiscards(deck, exps, ev, preflop):
    """Plays two hands with discards"""
    random.shuffle(deck)
    hole, board = [deck[:2], deck[2:4]], deck[4:7]
    exps[0][0].append(baseline.preflopexp(hole[0], preflop))
    exps[0][0].append(baseline.preflopexp(hole[1], preflop))
    drawtypes = [baseline.drawing(board, hole[0]),
                 baseline.drawing(board, hole[1])]
    exps[drawtypes[0]][1].append(baseline.evexp(board, hole[0], ev))
    exps[drawtypes[1]][1].append(baseline.evexp(board, hole[1], ev))
    for ind in range(2):
        toss = discard.flop(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[9 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[9 + ind]
    board = deck[4:8]
    drawtypes = [baseline.drawing(board, hole[0]),
                 baseline.drawing(board, hole[1])]
    exps[drawtypes[0]][2].append(baseline.evexp(board, hole[0], ev))
    exps[drawtypes[1]][2].append(baseline.evexp(board, hole[1], ev))
    for ind in range(2):
        toss = discard.turn(board, hole[ind], 1)
        if toss is not None:
            if toss == hole[ind][0]:
                hole[ind][0] = deck[11 + ind]
            elif toss == hole[ind][1]:
                hole[ind][1] = deck[11 + ind]
    board = deck[4:9]
    exps[0][3].append(baseline.evexp(board, hole[0], ev))
    exps[0][3].append(baseline.evexp(board, hole[1], ev))


def buckets():
    """Buckets"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    with open('ev.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    with open('preflop.pickle', 'rb') as handle:
        preflop = pickle.load(handle)
    print('starting')
    exps = [[[], [], [], []], [[], [], []]]
    for _ in range(10 ** 6):
        playdiscards(deck, exps, ev, preflop)
    exps[0][0] = sorted(exps[0][0])
    print([exps[0][0][len(exps[0][0]) * i // 40] for i in range(1, 40)])
    for ind1 in range(2):
        for ind2 in range(1, 3):
            exps[ind1][ind2] = sorted(exps[ind1][ind2])
            print([exps[ind1][ind2][len(exps[ind1][ind2]) * i // 20] for i in range(1, 20)])
    exps[0][3] = sorted(exps[0][3])
    print([exps[0][3][len(exps[0][3]) * i // 40] for i in range(1, 40)])

buckets()
