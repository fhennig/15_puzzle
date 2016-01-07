import numpy as np
import random
import heapq as q
import functools as f
import util as u
import operator 

# def str_dict(self):
#     d = dict()
#     for elem in self.elements():
#         elem1 = elem + 1
#         if elem1 == self.n()**2:
#             d.update({elem: "."})
#         else:
#             d.update({elem: str(elem1)})
#     return d
# 
# 
# def __str__(self):
#     d = self.str_dict()
#     w = len(max(d.values(), key=len))
#     strs = [d[e].rjust(w) for e in self.elements()]
#     a = u.list_to_array(strs)
#     lines = [" ".join(l) for l in a]
#     return "\n".join(lines)

    
### utility ###

def rotate(l, n=1):
    return l[n:] + l[:n]


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


def on_field(shape, coord):
    upper = all((np.array(coord) < np.array(shape)).flat)
    lower = all((np.array(coord) >= np.array(origin(len(shape)))).flat)
    return upper and lower


def puzzle_from_shape(shape):
    l = rotate(list(range(product(shape))))
    return from_list(l, shape)


def empty_position(p):
    return get_position(p, 0)


def get_position(p, element):
    return tuple(np.transpose(np.array(np.where(p == element)))[0])


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


def solved(p):
    """Gibt zurück wie das Puzzle gelöst aussehen müsste"""
    return from_list(rotate(sorted(p.flat)), p.shape)


def solvable(p):
    """Gibt an ob das Puzzle lösbar ist."""
    p1 = parity(p.flat, solved(p).flat)
    p2 = (-1)**u.manhattan_distance(self.n() - 1, self.n() -1, *self.empty_position())
    return p1 == p2


def is_solved(p):
    """Gibt an ob das Puzzle gelöst ist"""
    return all((p == solved(p)).flat)


### actions ###

def origin(dim):
    """0-Koordinate für gegebene Dimension"""
    return (0,) * dim


def direct_neighbors(coord):
    """Vierer-Nachbarschaft auf n Dimensionen"""
    orig = origin(len(coord))
    ns = []
    for i, v in enumerate(coord):
        n1 = list(orig)
        n1[i] = v + 1
        ns.append(tuple(n1))
        n2 = list(orig)
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


def reverse_action(a): # ??
    return tuple(np.array(a) * - 1)


def shuffle(p, n=1000):
    """Führt n zufällige Operationen aus"""
    for i in range(n):
        action = random.choice(possible_actions(p))
        p = apply_action(p, action)
    return p


### solvability ###

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
    while items:
        c = cycle(perm, items[0])
        cycles.append(c)
        items = [i for i in items if i not in c]
    transpositions = sum([len(c) - 1 for c in cycles])
    return (-1)**transpositions



### solver ###

def a_star(n, start, goal, obstacles):
    priority = lambda p: len(p) + u.manhattan_distance(*p[-1], *goal)
    visited = set()
    frontier = list()
    q.heappush(frontier, (priority([start]), [start]))
    while frontier:
        _, path = q.heappop(frontier)
        if path[-1] == goal:
            return path
        if not path[-1] in visited:
            visited.add(path[-1])
            walkable_neighbors = [nb for nb in u.four_neighbors(*path[-1])
                                  if on_field((n, n), nb) and nb not in obstacles]
            print(obstacles)
            print("walkable_neighbors:", walkable_neighbors)
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


    def execute(self, p, locked):
        l = locked.copy()
        l.add(self.locked_position())
        path = a_star(p.shape[0],
                      empty_position(p),
                      self.start_position, l)
        assert path, "PosAction not executable, starting position not reachable"
        actions = coords_to_actions(path)
        print("locked:", l)
        for a in actions:
            print("PosAction:", a)
            print(p)
            p = apply_action(p, a)
        p = apply_action(p, self.action)
        return p
        

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


def move_one_tile(p, tile, target_position, locked):
    """tile wird an position bewegt unter Berücksichtigung der locked Tiles
    tile: ein int
    locked: set von Positionen (Tupeln)"""
    start_position = get_position(p, tile)
    path = a_star(p.shape[0], start_position, target_position, locked)
    print(path)
    pos_actions = coords_to_pos_actions(path)
    print(pos_actions)
    for a in pos_actions:
        print("Meta-Action", a.start_position, a.action)
        print(p)
        p = a.execute(p, locked)
    return p


def solve(p):
    solved_pos = set()
    for i in [1, 2]:
        print("###### Moving Tile:", i),
        p = move_one_tile(p, i, get_position(solved(p), i), solved_pos)
        solved_pos.add(get_position(p, i))
    return p
        
