# coding: utf-8
from functools import reduce
from itertools import combinations, chain
from math import gcd
import numpy as np

#Lowest Common Multiple
def lcm(lcm_values):
    return reduce(lambda x,y: (lambda a,b: next(i for i in range(max(a,b),a*b+1) if i%a==0 and i%b==0))(x,y), lcm_values)

#factors
def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

#Get all combinations of factors
def combos_three(n):
    return combinations(n, 3)
#possibly not needed - for combos of two
def combos_two(n):
    return combinations(n, 2)

def rhythms(n):
    rhythm_options = []
    for i in list(n):
        x = reduce(gcd,i)
        if x == 1:
            rhythm_options.append(i)
    return rhythm_options

def rhythm_gen(lcm_values):
    x = lcm(lcm_values)
    n = factors(x)
    getcombos = combos_three(n)
    rhythmstuff = rhythms(getcombos)
    
    #sorts list and removes duplicates
    x = list(chain.from_iterable(rhythmstuff))
    x = list(set(x))
    x.sort()
    
    #subtracts bigger value from smaller from list of values
    a = np.array(x[::2])
    b = np.array(x[1::2])
    c = b - a
    
    return c
