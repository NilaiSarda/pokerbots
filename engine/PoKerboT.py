"""
==================================================
    Filename:   PoKerboT.py

 Description:   MIT pokerbots competition program

     Version:   1.0
     Created:   2017-01-19
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import argparse
import socket
import pickle
import bisect
import random
import baseline
import discard


SCRIMMING = False
NUM_ACTIONS = 3  # fold, check/call, bet/raise
POSTFLOP = [[0.23927613941018766, 0.2486021505376344, 0.25672087620311984, 0.26306046894282187, 0.26991978609625666, 0.2761804019617271, 0.2824620573355818, 0.2883817427385892, 0.2937363260675796, 0.2996744310935088, 0.3047914200153214, 0.3096836049856184, 0.3139647326507395, 0.31843998485422187, 0.32270916334661354, 0.32664013506994694, 0.3304809678371201, 0.3343181092302779, 0.33790523690773067, 0.3416134030602363, 0.34523580365736284, 0.3482472703390526, 0.35114351741174593, 0.35408131106208635, 0.3567402158157513, 0.3596902862505866, 0.36237806485631424, 0.36507307941536465, 0.36752674638137195, 0.37017572672031535, 0.3726108469971864, 0.37502092750711535, 0.37759980874970117, 0.37991724634204843, 0.3822521564457048, 0.38451443569553806, 0.3869402760200084, 0.38913854096949996, 0.3914983397897067, 0.39385234777888356, 0.39601304439301493, 0.39826404176363295, 0.4007897679619793, 0.40338661180566543, 0.4062049062049062, 0.40884674187017067, 0.41139240506329117, 0.4141174546049403, 0.41701054562127465, 0.4201099633455515, 0.4235728397629198, 0.426832700154777, 0.4306331006979063, 0.43414678317562366, 0.43748550220366506, 0.4412104936996488, 0.44475831763967355, 0.44872495446265936, 0.45295242491180643, 0.45746740673809216, 0.4620505992010652, 0.4660721791869333, 0.47034141196432255, 0.4741807348560079, 0.477802380293385, 0.4820463716572054, 0.48608940293841824, 0.49026676279740444, 0.4948410535876476, 0.4990037950664137, 0.503299935027186, 0.5080174927113703, 0.5134470874060681, 0.5195213853369143, 0.5251796333002974, 0.5311892061499843, 0.5381640337235001, 0.5452652159129547, 0.5526713709677419, 0.5605134474327629, 0.5692474015628556, 0.5774592761024341, 0.5849462365591398, 0.5926001219760114, 0.6001351960342497, 0.6083608360836084, 0.6189308176100629, 0.6297607099466483, 0.6413884364820847, 0.6535782938896417, 0.6647279307225022, 0.6770288088864027, 0.6900638103919782, 0.7034898272964566, 0.721014816137094, 0.741059323310536, 0.7900565552699229, 0.8531181112095428, 0.8784694742792538],
[0.06532416502946954, 0.08526315789473685, 0.10035949670461354, 0.11309800278680911, 0.12420382165605096, 0.13391812865497077, 0.14241960183767227, 0.1503184713375796, 0.15814696485623003, 0.16602440590879897, 0.17351816443594648, 0.18106995884773663, 0.18826340945300052, 0.19517543859649122, 0.20183741648106904, 0.20833333333333334, 0.2148014440433213, 0.2210970464135021, 0.22685185185185186, 0.2326073805202662, 0.23835125448028674, 0.24406175771971497, 0.2497893850042123, 0.255254931551148, 0.2610427226647357, 0.2670212765957447, 0.273224043715847, 0.27927927927927926, 0.28523936170212766, 0.2911764705882353, 0.2971241830065359, 0.30304127443881246, 0.3088235294117647, 0.31456320985033437, 0.32040609137055837, 0.32616487455197135, 0.3320556501987507, 0.33783783783783783, 0.3434343434343434, 0.34902309058614567, 0.35443037974683544, 0.35977954370674187, 0.36527377521613835, 0.3708690330477356, 0.37635054021608644, 0.3821782178217822, 0.3880952380952381, 0.3945489941596366, 0.4011183048852266, 0.40809968847352024, 0.41517857142857145, 0.421875, 0.42855029585798815, 0.4350152905198777, 0.4416899441340782, 0.44851348690687143, 0.4550743374272786, 0.46183118081180813, 0.4691358024691358, 0.4765446224256293, 0.48423112338858193, 0.49267782426778245, 0.5014577259475219, 0.5112431056427662, 0.5209643605870021, 0.5311158798283262, 0.5402374670184696, 0.5491891891891892, 0.5573927885641135, 0.5660112359550562, 0.5752532561505065, 0.5847791798107256, 0.5946681175190425, 0.6046868155935173, 0.6150442477876106, 0.6255115961800819, 0.6363636363636364, 0.6471387696709585, 0.6580459770114943, 0.6688650457722217, 0.679147465437788, 0.6883852691218131, 0.69740777666999, 0.7069672131147541, 0.717644694533762, 0.7288967822816548, 0.7405850977856796, 0.7580645161290323, 0.7755905511811023, 0.7921303970321256, 0.8073684789786485, 0.8275862068965517, 0.849610270518111, 0.8652778706614057, 0.8778613472858077, 0.8929133858267716, 0.916267942583732, 0.9330665696616952, 0.9642857142857143],
[0.010182207931404072, 0.019447287615148412, 0.027586206896551724, 0.037267080745341616, 0.04659685863874346, 0.05555555555555555, 0.06489361702127659, 0.07451403887688984, 0.08411214953271028, 0.09343664539653601, 0.10283818650939919, 0.11247216035634744, 0.12242090784044017, 0.13206459054209918, 0.14173228346456693, 0.15143992055610725, 0.16091395235780262, 0.17079646017699116, 0.1808259587020649, 0.19101123595505617, 0.20072992700729927, 0.21084097249900358, 0.22018970189701897, 0.2296606229660623, 0.2389846743295019, 0.24911971830985916, 0.25895316804407714, 0.26906435911303406, 0.27909176915799433, 0.2890834375558335, 0.2990936555891239, 0.30888575458392104, 0.31852741096438575, 0.32868352223190933, 0.33908582089552236, 0.35052192066805843, 0.36116152450090744, 0.3717948717948718, 0.3821656050955414, 0.39191489361702125, 0.4013772749631087, 0.4106813996316759, 0.4202827888834715, 0.43103448275862066, 0.4419525065963061, 0.4527363184079602, 0.4634146341463415, 0.47387033398821216, 0.48475909537856443, 0.4957107843137255, 0.5061274509803921, 0.5175400606323084, 0.5288574793875147, 0.539906103286385, 0.5505376344086022, 0.5607187112763321, 0.5706634930080333, 0.5799595141700404, 0.5893310753598645, 0.5993000874890638, 0.609674728940784, 0.6206896551724138, 0.6327705295471988, 0.6452191745706229, 0.657051282051282, 0.6678966789667896, 0.6786694101508917, 0.6887796887796888, 0.6990637539010254, 0.709279688513952, 0.719482619240097, 0.7305600870038064, 0.7418096723868954, 0.7528089887640449, 0.7639751552795031, 0.77390527256479, 0.7825022942795962, 0.7913086582947786, 0.8005830903790088, 0.8111702127659575, 0.822972972972973, 0.8343891402714932, 0.8472067483686138, 0.858250276854928, 0.8676503972758229, 0.8783382789317508, 0.8870599739243807, 0.8938924540827616, 0.9006211180124224, 0.9098998887652948, 0.9207920792079208, 0.9328859060402684, 0.9448621553884712, 0.9542140071222656, 0.9634464751958225, 0.9743406985032074, 0.9842661034846885, 0.9887758681164504, 0.9979674796747967]]


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


def run(input_socket):
    """NLHE Hold'em with discards"""
    f_in = input_socket.makefile()
    with open('ev2.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    with open('preflop.pickle', 'rb') as handle:
        preflop = pickle.load(handle)
    with open('nodes.pickle', 'rb') as handle:
        nodes = pickle.load(handle)
    with open('edge.pickle', 'rb') as handle:
        edge = pickle.load(handle)
    while True:
        data = f_in.readline().strip()
        if not data:
            print('Gameover, engine disconnected')
            break
        packet = data.split()
        if packet[0] == 'NEWGAME':
            name = packet[1]
            oppname = packet[2]
            if SCRIMMING:
                callrate = 3
            else:
                callrate = 2
            numhands = int(packet[5])
            allin = [0, 0]
            won = False
        elif packet[0] == 'NEWHAND':
            hole = [baseline.totuple(packet[3]), baseline.totuple(packet[4])]
            street, stack = 0, 199
            stack -= int(packet[2] == 'false')
            if SCRIMMING and int(packet[5]) - round(1.5 * numhands + 0.25) > 0:
                won = True
            numhands -= 1
            allin[1] += 1
            switch = False
        elif packet[0] == 'GETACTION':
            if won:
                s.send(b'CHECK\n')
                continue
            pot = int(packet[1])
            board, numboardcards = [], int(packet[2])
            for ind in range(numboardcards):
                board.append(baseline.totuple(packet[3 + ind]))
            lastactions, numlastactions = [], int(packet[3 + numboardcards])
            for ind in range(numlastactions):
                lastactions.append(packet[4 + numboardcards + ind])
            legalactions, numlegalactions = [], int(packet[4 + numboardcards + numlastactions])
            for ind in range(numlegalactions):
                legalactions.append(packet[5 + numboardcards + numlastactions + ind])
            for action in lastactions:
                if action[:7] == 'DISCARD' and name in action:
                    hole[hole.index(baseline.totuple(action[8:10]))] = baseline.totuple(action[11:13])
                elif action[:4] == 'DEAL':
                    if action == 'DEAL:FLOP':
                        street = 1
                    elif action == 'DEAL:TURN':
                        street = 2
                    elif action == 'DEAL:RIVER':
                        street = 3
            if 'DISCARD:' + baseline.tostr(hole[0]) in legalactions:
                decision = None
                if switch:
                    safety = 60
                else:
                    safety = 1
                if street == 1:
                    decision = discard.flop(board, hole, safety)
                elif street == 2:
                    decision = discard.turn(board, hole, safety)
                if decision is not None:
                    s.send(('DISCARD:' + baseline.tostr(decision) + '\n').encode())
                else:
                    s.send(b'CHECK\n')
            elif 400 - pot - stack < 110 and stack > 160:
                    allin[0] += 1
                    switch = True
                    if street == 0:
                        score = (1325 - edge.index(sorted(hole))) / 1326
                    else:
                        score = (100 - bisect.bisect(POSTFLOP[street - 1], baseline.evexp(board, hole, ev))) / 100
                    if score < 24 / 1326 or (allin[1] > 50 and score < allin[0] / allin[1] / callrate):
                        info = None
                        for action in legalactions:
                            if action[:5] == 'RAISE':
                                info = action.split(':')
                                break
                        if info is None:
                            s.send(b'CALL\n')
                        else:
                            stack = 0
                            s.send(('RAISE:' + info[2] + '\n').encode())
                    else:
                        s.send(b'CHECK\n')
            else:
                info = None
                for action in legalactions:
                    if action[:3] == 'BET' or action[:5] == 'RAISE':
                        info = action.split(':')
                        break
                if street == 0:
                    exp = baseline.preflopexp(hole, preflop)
                else:
                    exp = baseline.evexp(board, hole, ev)
                nodeind = baseline.findnode(street, 0, exp, [stack, 400 - pot - stack], board, hole)
                strat = nodes[nodeind].getavgstrat()
                choice = 0
                sample = random.random() - strat[choice]
                while sample > 0.0001:
                    choice += 1
                    sample -= strat[choice]
                # print(board, hole, exp, stack, 400 - pot - stack, strat, choice)
                if choice == 0:  # fold
                    s.send(b'CHECK\n')
                elif choice == 1:  # check/call
                    if 'CALL' in legalactions:
                        stack = 400 - pot - stack
                        s.send(b'CALL\n')
                    else:
                        s.send(b'CHECK\n')
                elif choice == 2:  # bet/raise
                    if info is None:
                        s.send(b'CALL\n')
                    else:
                        minraise = max(400 - pot - stack - int(info[2]) + int(info[1]), 0)
                        amt = max(pot - (200 - stack), 6)
                        bet = min(max(amt, minraise) + stack - (400 - pot - stack), stack)
                        stack -= bet
                        s.send((info[0] + ':' + str(int(info[2]) - stack) + '\n').encode())
        elif packet[0] == 'REQUESTKEYVALUES':
            s.send(b'FINISH\n')
    s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PKT pokerbot', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    print('Connecting to %s:%d' % (args.host, args.port))
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print('Error connecting! Aborting')
        exit()

    run(s)
