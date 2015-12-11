import numpy as np
import random
import math



ACTIONS = [(0, -1),
           (-1, 0),
           (0, +1),
           (+1, 0)]


class Puzzle:
    def __init__(self, **kwargs):
        if len(kwargs) > 1:
            raise ValueError("Only one keyword should be given: " + str(kwargs))
        if not kwargs:
            kwargs = {"dim": 4} # default action
        if "dim" in kwargs:
            dim = kwargs["dim"]
            l = list(range(1, dim**2))
            l.append(0)
            self._array = numberlist_to_array(l)
        elif "array" in kwargs:
            self._array = kwargs["array"]


    def empty_position(self):
        for y in range(self.dim()):
            for x in range(self.dim()):
                if self._array.item((y, x)) == 0:
                    return (y, x)
            

    def dim(self):
        return len(self._array)


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


    def solved(self):
        return all((self._array == init_array(self.dim())).flatten())


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
    v1 = array.item(tuple(p1))
    v2 = array.item(tuple(p2))
    array.itemset(tuple(p2), v1)
    array.itemset(tuple(p1), v2)
    

def on_field(size, x, y):
    """Testet ob die angegebe (x, y) Koordinate
    in einem Feld der Größe size * size liegt"""
    r = range(size)
    return x in r and y in r


def numberlist_to_array(ns):
    dim = math.sqrt(len(ns))
    rdim = round(dim)
    if dim != rdim:
        raise ValueError("Incorrect amount of elements given.")
    l = []
    for i in range(rdim):
        l.append(ns[i*rdim:(i+1)*rdim])
    return np.array(l)


def init_array(dim):
    l = list(range(1, dim**2))
    l.append(0)
    return numberlist_to_array(l)
    

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
