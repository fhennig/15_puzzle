import numpy as np



ACTIONS = [(0, -1),
           (-1, 0),
           (0, +1),
           (+1, 0)]


class Puzzle:
    def __init__(self, dim):
        self.dim = dim
        l = list(range(1, dim**2))
        l.append(0)
        l2 = []
        for i in range(dim):
            l2.append(l[i*dim:(i+1)*dim])
        self.array = np.array(l2)
        self.empty_spot = np.array((dim - 1, dim - 1))


    def possible_actions(self):
        return [a for a in ACTIONS
                if on_field(self.dim, *(self.empty_spot + a))]
        

    def apply_action(self, a):
        array_swap(self.array, self.empty_spot, self.empty_spot + a)
        self.empty_spot += a
        

    def __str__(self):
        return str(self.array)
        

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
