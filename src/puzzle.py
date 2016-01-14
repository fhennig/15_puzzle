import numpy as np
import random
import heapq as q
import functools as f
import util as u
import operator
from my_logging import log


    
### utility ### TODO potenziell auslagern

def manhattan_dist(c1, c2):
    assert len(c1) == len(c2), "Coordinates must be of same dimension"
    return sum(abs(np.array(c1) - c2))


def product(xs):
    return f.reduce(operator.mul, xs, 1)


def array_swap(array, p1, p2):
    """Vertauscht die Elemente an Position p1 und p2"""
    p1, p2 = tuple(p1), tuple(p2)
    v1 = array.item(p1)
    v2 = array.item(p2)
    a_new = array.copy()
    a_new.itemset(p2, v1)
    a_new.itemset(p1, v2)
    return a_new
    

def rotate(l, n=1):
    return l[n:] + l[:n]


def coord_to_index(coord, shape):
    index = 0
    for i, v in enumerate(coord):
        x = v * product(shape[i+1:])
        index += x
    return index


def from_list(l, shape):
    """Erstellt ein neues array mit der gegebenen shape und den Elementen aus l"""
    def f(*coords):
        index = coord_to_index(coords, shape)
        return l[index]
    return np.fromfunction(np.vectorize(f), shape, dtype=int)


### puzzle ###

def on_field(shape, coord):
    upper = all((np.array(coord) < np.array(shape)).flat)
    lower = all((np.array(coord) >= np.array(origin(len(shape)))).flat)
    return upper and lower


def puzzle_from_shape(shape):
    l = rotate(list(range(product(shape))))
    return from_list(l, shape)


def empty_position(p):
    return get_position(p, 0)


def empty_position_target(p):
    return tuple(np.array(p.shape) - 1)


def get_position(p, element):
    res = np.transpose(np.array(np.where(p == element)))
    assert product(res.shape) != 0, "Element {} not in Puzzle {}".format(element, p)
    return tuple(res[0])


### solvability ###

def solved(p):
    """Gibt zurück wie das Puzzle gelöst aussehen müsste"""
    return from_list(rotate(sorted(p.flat)), p.shape)


def is_solved(p):
    """Gibt an ob das Puzzle gelöst ist"""
    return all((p == solved(p)).flat)


def solvable(p):
    """Gibt an ob das Puzzle lösbar ist."""
    p1 = parity(p.flat, solved(p).flat)
    p2 = (-1)**manhattan_dist(empty_position(p), empty_position_target(p))
    return p1 == p2


def cycle(perm, init):
    """perm ist eine bijektion als Dictionary, init ist ein Element
    aus dem Bildraum. Gibt den Zyklus der Permutation zurück, der init enthält"""
    cycle = [init]
    while True:
        next = perm[cycle[-1]]
        if next == init:
            break
        cycle.append(next)
    return cycle


def parity(perm1, perm2):
    """perm1, perm2 Listen mit identischen Elementen aber (ggf)
    unterschiedlicher Reihenfolge der Elemente.
    Interpretiert perm2 als eine Permutation von perm1 und gibt
    die Parität dieser Permutation zurück."""
    perm = dict(zip(perm1, perm2))
    cycles = []
    items = perm1[:]
    while len(items) > 0:
        c = cycle(perm, items[0])
        cycles.append(c)
        items = [i for i in items if i not in c]
    transpositions = sum([len(c) - 1 for c in cycles])
    return (-1)**transpositions


### actions ###

def origin(dim):
    """0-Koordinate für gegebene Dimension"""
    return (0,) * dim


def direct_neighbors(coord):
    """Vierer-Nachbarschaft auf n Dimensionen"""
    ns = []
    for i, v in enumerate(coord):
        n1 = list(coord)
        n1[i] = v + 1
        ns.append(tuple(n1))
        n2 = list(coord)
        n2[i] = v - 1
        ns.append(tuple(n2))
    return ns

        
def actions(dim):
    return direct_neighbors(origin(dim))


def possible_actions(p):
    return [a for a in actions(len(p.shape))
            if on_field(p.shape, np.array(empty_position(p)) + a)]


def apply_action(p, a):
    ep = empty_position(p)
    return array_swap(p, ep, np.array(ep) + a)


def apply_actions(p, acts):
    for a in acts:
        p = apply_action(p, a)
    return p


def reverse_action(a): # ??
    return tuple(np.array(a) * - 1)


def shuffle(p, n=1000):
    """Führt n zufällige Operationen aus"""
    for i in range(n):
        action = random.choice(possible_actions(p))
        p = apply_action(p, action)
    return p


def random_puzzle(shape):
    l = list(range(product(shape)))
    while True:
        random.shuffle(l)
        p = from_list(l, shape)
        if solvable(p):
            return p
        
    
