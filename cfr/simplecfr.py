"""
==================================================
    Filename:   simplecfr.py

 Description:   Reduced number of actions

     Version:   1.0
     Created:   2017-01-24
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import pickle
import dbm
import random
import math
from poker import eval7
import discard
import baseline


ITERATIONS = 1000000
NUM_ACTIONS = 3  # fold, check/call, bet/raise


class Node():
    """Represents one information set"""

    def __init__(self):
        """Initialize variables"""
        self.regretsum = [0.0] * NUM_ACTIONS
        self.strat = [0.0] * NUM_ACTIONS
        self.stratsum = [0.0] * NUM_ACTIONS

    def getstrat(self, weight):
        """Gets current mixed strategy through regret matching"""
        for ind in range(NUM_ACTIONS):
            self.strat[ind] = self.regretsum[ind] * int(self.regretsum[ind] > 0)
        normalizingsum = sum(self.strat)
        for ind in range(NUM_ACTIONS):
            if normalizingsum > 0:
                self.strat[ind] /= normalizingsum
            else:
                self.strat[ind] = 1.0 / NUM_ACTIONS
            self.stratsum[ind] += weight * self.strat[ind]
        return self.strat

    def getavgstrat(self):
        """Gets average mixed strategy across all training iterations"""
        avgstrat = [1.0 / NUM_ACTIONS] * NUM_ACTIONS
        normalizingsum = sum(self.stratsum)
        if normalizingsum > 0:
            avgstrat = [a / normalizingsum for a in self.stratsum]
        return avgstrat


def simplecfr(street, button, minraise, stack, p, nodes, boards, holes, winner, tie, exps):
    """One iteration"""
    player = button % 2
    opp = 1 - player
    # return payoff for terminal states
    if stack[0] == stack[1] and ((street == 0 and button > 1) or (street > 0 and button > 2)):
        if stack[0] == 0 or street == 3:  # all in or river
            if tie:
                return 0
            return (200 - stack[0]) * (2 * int(player == winner) - 1)
        return simplecfr(street + 1, 1, 2, stack, p, nodes, boards, holes, winner, tie, exps) * (2 * player - 1)
    # for each action, recursively call cfr with additional history and probability
    nodeind = baseline.findnode(street, player, exps[player][street], stack, boards[street], holes[player][street])
    strat = nodes[nodeind].getstrat(p[player])
    util = [0.0] * NUM_ACTIONS
    nodeutil = 0.0
    if (street == 0 and button > 3) or (street > 0 and button > 4):
        for ind in range(NUM_ACTIONS):
            if ind == 0:
                util[ind] = stack[player] - 200
            else:
                tmpp = list(p)
                tmpp[player] *= strat[ind]
                util[ind] = -1 * simplecfr(street, button + 1, minraise, [stack[opp], stack[opp]], tmpp, nodes, boards, holes, winner, tie, exps)
            nodeutil += strat[ind] * util[ind]
    else:
        for ind in range(NUM_ACTIONS):
            if ind == 0:  # fold
                util[ind] = stack[player] - 200
            else:
                if ind == 1:  # check/call
                    bet = stack[player] - stack[opp]
                    tmpminraise = minraise
                elif ind == 2:  # bet/raise
                    lim = max(200 - stack[opp], 6)
                    amt = round(random.gauss(lim, lim))
                    bet = min(max(amt, minraise) + stack[player] - stack[opp], stack[player])
                    tmpminraise = bet - (stack[player] - stack[opp])
                tmpstack, tmpp = list(stack), list(p)
                tmpstack[player] -= bet
                tmpp[player] *= strat[ind]
                util[ind] = -1 * simplecfr(street, button + 1, tmpminraise, tmpstack, tmpp, nodes, boards, holes, winner, tie, exps)
            nodeutil += strat[ind] * util[ind]
    # for each action, compute and accumulate counterfactual regret
    for ind in range(NUM_ACTIONS):
        regret = util[ind] - nodeutil
        nodes[nodeind].regretsum[ind] += p[opp] * regret
    return nodeutil


def cfrcrunch():
    """Plays hands on hands on hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    # nodes = []
    # for _ in range(1600):
        # nodes.append(Node())
    with open('nodes.pickle', 'rb') as handle:
        nodes = pickle.load(handle)
    with open('preflop.pickle', 'rb') as handle:
        preflop = pickle.load(handle)
    db = dbm.open('evdb', 'r')
    for _ in range(ITERATIONS):
        random.shuffle(deck)
        boards = [[], deck[4:7], deck[4:8], deck[4:9]]
        holes = [[deck[:2], deck[:2], deck[:2], deck[:2]], [deck[2:4], deck[2:4], deck[2:4], deck[2:4]]]
        for ind in range(2):
            toss = discard.flop(boards[1], holes[ind][1], 1)
            if toss is not None:
                if toss == holes[ind][1][0]:
                    holes[ind][1][0] = deck[9 + ind]
                    holes[ind][2][0] = deck[9 + ind]
                    holes[ind][3][0] = deck[9 + ind]
                elif toss == holes[ind][1][1]:
                    holes[ind][1][1] = deck[9 + ind]
                    holes[ind][2][1] = deck[9 + ind]
                    holes[ind][3][1] = deck[9 + ind]
        for ind in range(2):
            toss = discard.turn(boards[2], holes[ind][2], 1)
            if toss is not None:
                if toss == holes[ind][2][0]:
                    holes[ind][2][0] = deck[11 + ind]
                    holes[ind][3][0] = deck[11 + ind]
                elif toss == holes[ind][2][1]:
                    holes[ind][2][1] = deck[11 + ind]
                    holes[ind][3][1] = deck[11 + ind]
        tmpboard = [baseline.tostr(c) for c in boards[3]]
        tmphole = [[baseline.tostr(c) for c in holes[0][3]], [baseline.tostr(c) for c in holes[1][3]]]
        score0 = eval7(tmpboard + tmphole[0])
        score1 = eval7(tmpboard + tmphole[1])
        winner = int(score0 > score1)
        tie = (score0 == score1)
        exps = [[], []]
        for ind1 in range(2):
            exps[ind1].append(baseline.preflopexp(holes[ind1][0], preflop))
            for ind2 in range(1, 4):
                exps[ind1].append(float(db.get(str(baseline.evkeygen(boards[ind2], holes[ind1][ind2])), b'0.5').decode()))
        simplecfr(0, 0, 2, [198, 198], [1.0, 1.0], nodes, boards, holes, winner, tie, exps)
    for ind, node in enumerate(nodes):
        print(ind, node.regretsum, node.strat, node.stratsum)
    with open('nodes.pickle', 'wb') as handle:
        pickle.dump(nodes, handle, protocol=pickle.HIGHEST_PROTOCOL)

cfrcrunch()
