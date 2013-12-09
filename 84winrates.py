import math
import numpy as np
import matplotlib.pyplot as plt

def elo_winrate(diff): return 1-1/(10**(float(diff)/400.0)+1)

MY_RATING = 1769
N = 100
AVE_RATING = 1670
SIGMA = 60

def make_p0(n,mu,sigma, breadth=4):
    ratings = [mu]
    for i in range(1,n/2):
        ratings.append(mu + 2*breadth*sigma*i/n) 
        ratings.append(mu - 2*breadth*sigma*i/n) 
    ratings.sort()
    p_temp = [math.exp(-(float(x-mu))**2/(2*sigma**2)) for x in ratings]
    total = sum(p_temp)
    p_0 = [p/total for p in p_temp]
    return ratings,p_0

ratings,p_0 = make_p0(N,AVE_RATING,SIGMA)

if sum(p_0) > 1.0001 or sum(p_0) < 0.9999:
    print "NONNORMALIZED DIST"
if len(ratings)!=len(p_0): print 'INVALID DIST'

def winrate(probs) : return sum([probs[i]*elo_winrate(MY_RATING - ratings[i]) for i in range(len(ratings))])

def next_round(probs): return [2*probs[i]*sum([probs[j]*elo_winrate(ratings[i]-ratings[j]) for j in range(len(ratings))])
                     for i in range(len(ratings))]

def n_rounds(p, n):
    for j in range(n):
        p = next_round(p)
    return p

p = p_0
w = []
for n in range(3):
    plt.plot(ratings,p)
    p = n_rounds(p,1)
    w.append(winrate(p))

for item in w:
    print item
    
plt.show()



