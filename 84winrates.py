import math
import numpy as np
import matplotlib.pyplot as plt

def elo_winrate(diff): return 1-1/(10**(float(diff)/400.0)+1)

MY_RATING = 1769
N = 48
AVE_RATING = 1680
SIGMA = 60
BREADTH = 4

def make_p0(n,mu,sigma, breadth):
    ratings = [mu]
    for i in range(1,n/2):
        ratings.append(mu + 2*breadth*sigma*i/n) 
        ratings.append(mu - 2*breadth*sigma*i/n) 
    ratings.sort()
    p_temp = [math.exp(-(float(x-mu))**2/(2*sigma**2)) for x in ratings]
    total = sum(p_temp)
    p_0 = [p/total for p in p_temp]
    return ratings,p_0

ratings,p_0 = make_p0(N,AVE_RATING,SIGMA,BREADTH)

if sum(p_0) > 1.0001 or sum(p_0) < 0.9999:
    print "NONNORMALIZED DIST"
if len(ratings)!=len(p_0): print 'INVALID DIST'

def winrate(probs) : return sum([probs[i]*elo_winrate(MY_RATING - ratings[i])
                                 for i in range(len(ratings))])

def next_round(probs): return [2*probs[i]*sum([probs[j]*elo_winrate(
                    ratings[i]-ratings[j]) for j in range(len(ratings))])
                     for i in range(len(ratings))]

def n_rounds(p, n):
    for j in range(n):
        p = next_round(p)
    return p

p = p_0

plt.ylabel('proportion of ' + str(SIGMA/2) + ' point interval')
plt.xlabel('Elo rating')

for n in range(3):
    k=1
    plt.plot(ratings,[el*N/(4*BREADTH) for el in p],
             label = 'Rd '+str(k*n+1)+' wr = ' + str("{0:.3f}".format(
                                                     round(winrate(p),3))))
    p = n_rounds(p,k)


plt.legend(loc=2)
plt.show()



