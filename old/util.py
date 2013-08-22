import math

def subsets(set_):
    LARGEST = 2
    if LARGEST >= len(set_)/2:
        return(subsets_up_to_size(set_, len(set_)))
    else: return subsets_up_to_size(set_, LARGEST)+ \
         subsets_larger_than_size(set_, len(set_)-LARGEST)

def subsets_up_to_size(set_, number):
    subset = [[]]
    if number == 0:
        return subset
    new_set = list(set_)
    for item in set_:
        new_set.remove(item)
        subset = subset + [[item] + subs for subs in subsets_up_to_size(new_set,
                                             min([len(new_set),number-1]))]
    return subset    

def subsets_larger_than_size(set_, number):
    subset = []
    new_set = list(set_)
    if number == 0:
        return subsets_up_to_size(set_, len(set_))
    for item in set_:
        new_set.remove(item)
        if len(new_set)>=number-1:
            subset = subset + [[item] + subs for subs in \
                               subsets_larger_than_size(new_set, number-1)]
    return subset

def choose(n, k):
    j = min(k, n-k)
    prod = 1
    for i in range(j):
        prod = prod*(n-i)
    return prod/math.factorial(j)

