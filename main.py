import numpy as np
import random
import scipy.optimize as opt
import pandas as pd
from statistics import mean, stdev
import matplotlib.pyplot as plt
import math

# Number of Men or Women
MAX_SIZE = int(input("Input maximum set size >3 for simulation: "))
NUM_SIMS = int(input("Input number of simulations for each size (recommended 500-1000): "))
SCORING = input("Input scoring method ('add', 'mult', or 'root'): ")
MAN_WEIGHT = float(input("Input weighting for man/proposer: "))
WOMAN_WEIGHT = float(input("Input weighting for woman/accepter: "))
SCORING = SCORING.lower()
if SCORING != 'add' and SCORING != 'mult' and SCORING != 'root':
    raise ValueError('Scoring method must be add, mult, or root')

# This function returns true if
# woman 'w' prefers man 'm1' over man 'm'
def wPrefersM1OverM(prefer, w, m, m1):
    # Check if w prefers m over her
    # current engagement m1
    for i in range(N):

        # If m1 comes before m in list of w,
        # then w prefers her current engagement,
        # don't do anything
        if (prefer[w][i] == m1):
            return True

        # If m comes before m1 in w's list,
        # then free her current engagement
        # and engage her with m
        if (prefer[w][i] == m):
            return False


# Prints stable matching for N boys and N girls.
# Boys are numbered as 0 to N-1.
# Girls are numbered as N to 2N-1.
def stableMarriage(prefer):
    # Stores partner of women. This is our output
    # array that stores passing information.
    # The value of wPartner[i] indicates the partner
    # assigned to woman N+i. Note that the woman numbers
    # between N and 2*N-1. The value -1 indicates
    # that (N+i)'th woman is free
    wPartner = [-1 for i in range(N)]

    # An array to store availability of men.
    # If mFree[i] is false, then man 'i' is free,
    # otherwise engaged.
    mFree = [False for i in range(N)]

    freeCount = N

    # While there are free men
    while (freeCount > 0):

        # Pick the first free man (we could pick any)
        m = 0
        while (m < N):
            if (mFree[m] == False):
                break
            m += 1

        # One by one go to all women according to
        # m's preferences. Here m is the picked free man
        i = 0
        while i < N and mFree[m] == False:
            w = prefer[m][i]

            # The woman of preference is free,
            # w and m become partners (Note that
            # the partnership maybe changed later).
            # So we can say they are engaged not married
            if (wPartner[w - N] == -1):
                wPartner[w - N] = m
                mFree[m] = True
                freeCount -= 1

            else:

                # If w is not free
                # Find current engagement of w
                m1 = wPartner[w - N]

                # If w prefers m over her current engagement m1,
                # then break the engagement between w and m1 and
                # engage m with w.
                if (wPrefersM1OverM(prefer, w, m, m1) == False):
                    wPartner[w - N] = m
                    mFree[m] = True
                    mFree[m1] = False
            i += 1

        # End of Else
    # End of the for loop that goes
    # to all women in m's list
    # End of main while loop

    # Print solution
    # print("Woman ", " Man")
    # for i in range(N):
    #    print(i + N, "\t", wPartner[i])

    mtotscore = 0
    wtotscore = 0
    total = 0
    for i in range(N):
        wscore = 1 + prefer[i + N].index(wPartner[i])
        mscore = 1 + prefer[wPartner[i]].index(i + N)
        if SCORING == 'add':
            mtotscore += mscore
            wtotscore += wscore
            total += ((MAN_WEIGHT * mscore) + (WOMAN_WEIGHT  * wscore))
        elif SCORING == 'mult':
            mtotscore += mscore
            wtotscore += wscore
            total += ((MAN_WEIGHT * mscore) * (WOMAN_WEIGHT * wscore))
        elif SCORING == 'root':
            mtotscore += math.sqrt(mscore)
            wtotscore += math.sqrt(wscore)
            total += ((MAN_WEIGHT * math.sqrt(mscore)) + (WOMAN_WEIGHT * math.sqrt(wscore)))
    return total, mtotscore, wtotscore


# Driver Code


df = pd.DataFrame()

for a in range(3, MAX_SIZE + 1):
    gs = []
    hung = []
    mgs = []
    wgs = []
    mh = []
    wh = []
    print(a)
    for b in range(NUM_SIMS + 1):
        N = a
        manpref = []
        womanpref = []
        for i in range(N):
            w = np.arange(start=0, stop=N, step=1).tolist()
            m = np.arange(start=N, stop=2 * N, step=1).tolist()
            random.shuffle(w)
            random.shuffle(m)
            manpref.append(m)
            womanpref.append(w)

        smprefer = manpref
        smprefer.extend(womanpref)
        hungprefer = np.empty((N, N))
        manhung = np.empty((N, N))
        womanhung = np.empty((N, N))

        for i in range(N):
            for j in range(N):
                if SCORING == 'add':
                    hungprefer[i][j] = (MAN_WEIGHT * (1 + smprefer[i].index(j + N))) + (WOMAN_WEIGHT * (1 + smprefer[j + N].index(i)))
                    manhung[i][j] = 1 + smprefer[i].index(j + N)
                    womanhung[i][j] = 1 + smprefer[j + N].index(i)
                elif SCORING == 'mult':
                    hungprefer[i][j] = MAN_WEIGHT * (1 + smprefer[i].index(j + N)) * WOMAN_WEIGHT * (1 + smprefer[j + N].index(i))
                    manhung[i][j] = 1 + smprefer[i].index(j + N)
                    womanhung[i][j] = 1 + smprefer[j + N].index(i)
                elif SCORING == 'root':
                    hungprefer[i][j] = (MAN_WEIGHT * math.sqrt(1 + smprefer[i].index(j + N))) + (WOMAN_WEIGHT * math.sqrt(1 + smprefer[j + N].index(i)))
                    manhung[i][j] = math.sqrt(1 + smprefer[i].index(j + N))
                    womanhung[i][j] = math.sqrt(1 + smprefer[j + N].index(i))




        tot_score, man_score, w_score = stableMarriage(smprefer)
        row_ind, col_ind = opt.linear_sum_assignment(hungprefer)
        hungscore = hungprefer[row_ind, col_ind].sum()
        m_h_score = manhung[row_ind, col_ind].sum()
        w_h_score = womanhung[row_ind, col_ind].sum()
        gs.append(tot_score)
        hung.append(hungscore)
        mgs.append(man_score)
        wgs.append(w_score)
        mh.append(m_h_score)
        wh.append(w_h_score)

    print('gs: ', mean(gs), 'hung', mean(hung))

    df = df.append({'N': N, 'gs_mean': mean(gs), 'gs_sd': stdev(gs), 'hung_mean': mean(hung), 'hung_sd': stdev(hung),
                    'gs_man_mean': mean(mgs), 'gs_w_mean': mean(wgs), 'gs_man_sd': stdev(mgs), 'gs_w_sd': stdev(wgs),
                    'h_man_mean': mean(mh), 'h_man_sd': stdev(mh), 'h_w_mean': mean(wh), 'h_w_sd': stdev(wh)},
                   ignore_index=True)

df.to_csv('gs_results.csv')

gs1 = df['gs_mean'] + df['gs_sd']
gs2 = df['gs_mean'] - df['gs_sd']

h1 = df['hung_mean'] + df['hung_sd']
h2 = df['hung_mean'] - df['hung_sd']


fig, ax = plt.subplots()
ax.plot(df['N'], df['gs_mean'])
ax.fill_between(df['N'], gs2, gs1, color='b', alpha=.1)
ax.plot(df['N'], df['hung_mean'])
ax.fill_between(df['N'], h2, h1, color='y', alpha=.1)
ax.legend(['Gale Shapely', 'Hungarian'])
plt.xlabel('Bipartite Set Size')
plt.ylabel('Score')
title = 'Mean +- 1 Stdev for Scoring Method: ' + SCORING + ', with man weighting: ' + str(MAN_WEIGHT) + ' and woman weighting: ' + str(WOMAN_WEIGHT) + ', for ' + str(NUM_SIMS) + ' simulations'
plt.title(title)
plt.show()

fig, ax = plt.subplots()
ax.plot(df['N'], df['gs_man_mean'])
ax.plot(df['N'], df['gs_w_mean'])
ax.plot(df['N'], df['h_man_mean'])
ax.plot(df['N'], df['h_w_mean'])
ax.legend(['GS Man', "GS Woman", "Hung Man", "Hung Woman"])
plt.xlabel('Bipartite Set Size')
plt.ylabel('Score')
title = 'Bipartite Results for Scoring Method: ' + SCORING + ', with man weighting: ' + str(MAN_WEIGHT) + ' and woman weighting: ' + str(WOMAN_WEIGHT) + ', for ' + str(NUM_SIMS) + ' simulations'
plt.title(title)
plt.show()