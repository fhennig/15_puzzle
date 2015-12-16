import numpy as np
import random
import math
import heapq as q
import functools



ACTIONS = [(0, -1),
           (-1, 0),
           (0, +1),
           (+1, 0)]


class Puzzle:
    """Zustand ist nur ein numpy-Array self._array
    immutable"""
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
        return self.get_position(self.movable_element())


    def get_position(self, element):
        for y in range(self.dim()):
            for x in range(self.dim()):
                if self._array.item((y, x)) == element:
                    return (y, x)


    def possible_actions(self):
        return [a for a in ACTIONS
                if on_field(self.dim(), *(np.array(self.empty_position()) + a))]
        

    def apply_action(self, a):
        assert a in ACTIONS, "action is not a valid action: %r" % a
        p = self.empty_position()
        return Puzzle(array=array_swap(self._array, p, np.array(p) + a))


    def shuffle(self, n=1000): ## TODO auslagern
        """Führt n zufällige Operationen aus"""
        p = self
        for i in range(n):
            action = random.choice(p.possible_actions())
            p = p.apply_action(action)
        return p


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


    def solved_state(self):
        return Puzzle(dim=self.dim())


    def __eq__(self, other):
        return self.array == other.array

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._array)


    ## string representation ##

    def str_dict(self):
        d = dict()
        for elem in self.elements():
            elem1 = elem + 1
            if elem1 == self.dim()**2:
                d.update({elem: "."})
            else:
                d.update({elem: str(elem1)})
        return d

    
    def __str__(self):
        d = self.str_dict()
        w = len(max(d.values(), key=len))
        strs = [d[e].rjust(w) for e in self.elements()]
        a = list_to_array(strs)
        lines = [" ".join(l) for l in a]
        return "\n".join(lines)

    
    def __repr__(self): ## TODO maybe better representation like np.array has
        return str(self)


### utility ###


def array_swap(array, p1, p2):
    """Vertauscht die Elemente an Position p1 und p2"""
    p1, p2 = tuple(p1), tuple(p2)
    v1 = array.item(p1)
    v2 = array.item(p2)
    a_new = array.copy()
    a_new.itemset(p2, v1)
    a_new.itemset(p1, v2)
    return a_new
    

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
#    assert sorted(perm1) == sorted(perm2)
    perm = dict(zip(perm1, perm2))
    cycles = []
    items = perm1[:]
    while items:
        c = cycle(perm, items[0])
        cycles.append(c)
        items = [i for i in items if i not in c]
    transpositions = sum([len(c) - 1 for c in cycles])
    return (-1)**transpositions


### solver ###
    
        
def four_neighbors(x, y):
    return [(x - 1, y),
            (x, y - 1),
            (x + 1, y),
            (x, y + 1)]


def a_star(dim, start, goal, obstacles):
    priority = lambda p: len(p) + manhattan_distance(*p[-1], *goal)
    visited = set()
    frontier = list()
    q.heappush(frontier, (priority([start]), [start]))
    while frontier:
        _, path = q.heappop(frontier)
        if path[-1] == goal:
            return path
        if not path[-1] in visited:
            visited.add(path[-1])
            walkable_neighbors = [n for n in four_neighbors(*path[-1])
                                  if on_field(dim, *n) and n not in obstacles]
            for p in [path + [n] for n in walkable_neighbors]:
                q.heappush(frontier, (priority(p), p))
    return None


class PosAction:
    """Beschreibt eine Aktion die an einer bestimmten Position ausgeführt werden soll."""
    def __init__(self, start, action):
        self.start_position = start
        self.action = action

        
    def locked_position(self):
        return tuple(np.array(self.start_position) + self.action)


    def execute(self, puzzle, locked):
        l = locked.copy()
        l.add(self.locked_position())
        path = a_star(puzzle.dim(),
                      puzzle.get_position(puzzle.movable_element()),
                      self.start_position, l)
        assert path, "PosAction not executable, starting position not reachable"
        actions = coords_to_actions(path)
        print("locked:", l)
        for a in actions:
            print("PosAction:", a)
            print(puzzle)
            puzzle = puzzle.apply_action(a)
        puzzle = puzzle.apply_action(self.action)
        return puzzle
        

def coords_to_actions(coords):
    actions = []
    for i in range(1, len(coords)):
        action = tuple(np.array(coords[i]) - np.array(coords[i - 1]))
        actions.append(action)
    return actions
        

def coords_to_pos_actions(coords):
    actions = []
    for i in range(1, len(coords)):
        action = tuple(np.array(coords[i - 1]) - np.array(coords[i]))
        a = PosAction(coords[i], action)
        actions.append(a)
    return actions


def move_one_tile(puzzle, tile, target_position, locked):
    """tile wird an position bewegt unter Berücksichtigung der locked Tiles
    tile: ein int
    locked: set von Positionen (Tupeln)"""
    start_position = puzzle.get_position(tile)
    print("start pos:", start_position)
    path = a_star(puzzle.dim(), start_position, target_position, locked)
    pos_actions = coords_to_pos_actions(path)
    for a in pos_actions:
        print("Meta-Action", a.start_position, a.action)
        print(puzzle)
        puzzle = a.execute(puzzle, locked)
    return puzzle


def solve(puzzle):
    solved = set()
    for i in [0, 1, 4]:
        print("###### Moving Tile:", i),
        puzzle = move_one_tile(puzzle, i, puzzle.solved_state().get_position(i), solved)
        solved.add(i)
    return puzzle
        
