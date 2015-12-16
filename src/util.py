import math
import numpy as np



def list_to_array(ns): ## TODO shape als Parameter entgegen nehmen 
    """Erstellt aus einer Liste von Elementen ein quadratisches Array."""
    dim = math.sqrt(len(ns))
    rdim = round(dim)
    if dim != rdim:
        raise ValueError("Incorrect amount of elements given.")
    l = []
    for i in range(rdim):
        l.append(ns[i*rdim:(i+1)*rdim])
    return np.array(l)


def array_to_list(a):
    """Erstellt aus einem Array eine Liste."""
    return list(a.flatten())


def a_sorted(array):
    return list_to_array(sorted(array_to_list(array)))
    

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def four_neighbors(x, y):
    return [(x - 1, y),
            (x, y - 1),
            (x + 1, y),
            (x, y + 1)]
