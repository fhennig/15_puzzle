import numpy as np
import random
import math



ACTIONS = [(0, -1),
           (-1, 0),
           (0, +1),
           (+1, 0)]


class Puzzle:
    """Zustand ist nur ein numpy-Array self._array"""
    def __init__(self, **kwargs):
        if len(kwargs) > 1:
            raise ValueError("Only one keyword should be given: " + str(kwargs))
        if not kwargs:
            kwargs = {"dim": 4} # default action
        if "dim" in kwargs:
            dim = kwargs["dim"]
            self._array = init_array(dim)
        elif "array" in kwargs:
            self._array = kwargs["array"]
            

    def dim(self):
        return len(self._array)


    def elements(self):
        return array_to_list(self._array)
    

    def movable_element(self):
        return self.dim()**2 - 1


    def empty_position(self):
        for y in range(self.dim()):
            for x in range(self.dim()):
                if self._array.item((y, x)) == self.movable_element():
                    return (y, x)


    def possible_actions(self):
        return [a for a in ACTIONS
                if on_field(self.dim(), *(np.array(self.empty_position()) + a))]
        

    def apply_action(self, a):
        assert a in ACTIONS, "action is not a valid action: %r" % a
        p = self.empty_position()
        array_swap(self._array, p, np.array(p) + a)


    def shuffle(self, n=1000):
        """Führt n zufällige Operationen aus"""
        for i in range(n):
            action = random.choice(self.possible_actions())
            self.apply_action(action)


    def solvable(self):
        """Gibt an ob das Puzzle lösbar ist."""
        l1, l2 = [array_to_list(a) for a in [self._array, init_array(self.dim())]]
        p1 = parity(array_to_list(self._array),
                    array_to_list(init_array(self.dim())))
        p2 = (-1)**manhattan_distance(self.dim() - 1, self.dim() -1, *self.empty_position())
        return p1 == p2
            

    def solved(self):
        """Gibt an ob das Puzzle gelöst ist"""
        return all((self._array == a_sorted(self._array)).flatten())


    def __eq__(self, other):
        return self.array == other.array

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._array)

    def __str__(self):
        return str(self._array)

    def __repr__(self):
        return str(self._array)
        

def array_swap(array, p1, p2):
    """Vertauscht die Elemente an Position p1 und p2"""
    p1, p2 = tuple(p1), tuple(p2)
    v1 = array.item(p1)
    v2 = array.item(p2)
    array.itemset(p2, v1)
    array.itemset(p1, v2)
    

def on_field(size, x, y):
    """Testet ob die angegebe (x, y) Koordinate
    in einem Feld der Größe size * size liegt"""
    r = range(size)
    return x in r and y in r


def init_array(dim):
    l = list(range(dim**2))
    return list_to_array(l)


def list_to_array(ns):
    dim = math.sqrt(len(ns))
    rdim = round(dim)
    if dim != rdim:
        raise ValueError("Incorrect amount of elements given.")
    l = []
    for i in range(rdim):
        l.append(ns[i*rdim:(i+1)*rdim])
    return np.array(l)


def array_to_list(a):
    return list(a.flatten())


def a_sorted(array):
    return list_to_array(sorted(array_to_list(array)))
    

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


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
    assert sorted(perm1) == sorted(perm2)
    perm = dict(zip(perm1, perm2))
    cycles = []
    items = perm1[:]
    while items:
        c = cycle(perm, items[0])
        cycles.append(c)
        items = [i for i in items if i not in c]
    transpositions = sum([len(c) - 1 for c in cycles])
    return (-1)**transpositions
