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
            walkable_neighbors = [nb for nb in direct_neighbors(path[-1])
                                  if on_field((n, n), nb) and nb not in obstacles]
            for p in [path + [n] for n in walkable_neighbors]:
                q.heappush(frontier, (priority(p), p))
    return None


class PosAction:
    """Beschreibt eine Aktion die an einer bestimmten Position ausgeführt werden soll."""
    def __init__(self, start, actions):
        self.start_position = start
        self.actions = actions

        
    def locked_position(self):
        return tuple(np.array(self.start_position) + self.actions[0])


    def execute(self, p, locked):
        """p: das Feld auf dem die Aktion ausgeführt werden soll
        locked: eine Menge von Positionen die nicht bewegt werden dürfen. 
        Die erste Position die durch die Aktion betreten wird, wird autoamtisch gelockt"""
        log.debug("executing PosAction; start: {}, actions: {}".format(self.start_position,
                                                                       self.actions))
        l = locked.copy()
        l.add(self.locked_position()) # die erste Position wird automatisch gelockt!
        path = a_star(p.shape[0],
                      empty_position(p),
                      self.start_position, l)
        assert path, "PosAction not executable, starting position not reachable"
        init_actions = coords_to_actions(path)
#        log.info("moving into start pos., path: {}".format(init_actions))
        p = apply_actions(p, init_actions)
        p = apply_actions(p, self.actions)
        return p, init_actions + self.actions
        

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
        a = PosAction(coords[i], [action])
        actions.append(a)
    return actions


def move_one_tile(p, tile, target_position, locked):
    """tile wird an position bewegt unter Berücksichtigung der locked Tiles
    tile: ein int
    locked: set von Positionen (Tupeln)"""
    start_position = get_position(p, tile)
    path = a_star(p.shape[0], start_position, target_position, locked)
#    print(path)
    pos_actions = coords_to_pos_actions(path)
#    print(pos_actions)
    actions = []
    for a in pos_actions:
#        print("Meta-Action", a.start_position, a.actions)
#        print(p)
        p, acts = a.execute(p, locked)
        actions += acts
    return p, actions


def transpose_action(a):
    """tauscht x und y Achse der action"""
    return tuple(reversed(a))


class SolverStruct:
    """Klasse um die oberste Reihe eines Puzzles zu lösen"""
    def __init__(self, p, moves, transp = False):
        self.locked = set()
        self.transposed = transp
        self.p = p.transpose() if transp else p
        self.s = solved(p).transpose() if transp else solved(p)
        self._moves = [transpose_action(m) for m in moves] if transp else moves


    def get_target_positions(self):
        """Gibt ein dict zurück, dass alle bis auf das letzte Element der zu lösenden 
        Reihe auf ihre gewünschte Position abbildet"""
        l = list(self.s[0])
        d = dict()
        for i in l[:-2]:
            d.update({i: get_position(self.s, i)})
        # besondere Position für den Vorletzten
        d.update({l[-2]: tuple(np.array(get_position(self.s, l[-2])) + (0, 1))})
        return d


    def solve_but_last(self):
        """Löst die ersten n-2 der obersten Reihe und bringt den n-1ten in eine
        geeignete Position um ihn zusammen mit dem n-ten zu lösen (z.B.: '12.3')"""
        d = self.get_target_positions()
        for i in sorted(d):
            log.info("solving element {}".format(i))
            self.p, acts = move_one_tile(self.p, i, d[i], self.locked)
            self._moves += acts
            self.locked.add(get_position(self.p, i))


    def lst_pos(self):
        """Gibt die aktuelle Position des letzten zu lösenden Elements zurück"""
        last = self.s[0][-1]
        return get_position(self.p, last)


    def stl_pos(self):
        """Gibt die aktuelle Position des vorletzten zu lösenden Elements zurück"""
        stl = self.s[0][-2]
        return get_position(self.p, stl)


    def exec_pa(self, pa, locked):
        self.p, acts = pa.execute(self.p, locked)
        self._moves += acts

        
    def solve_last(self):
#        log.info("solving last:\n{}",format(self.p))
        """Löst die letzten beiden Elemente, womit dann die ganze Reihe gelöst ist"""
        r, d, l, u = (0, 1), (1, 0), (0, -1), (-1, 0)
        final_lst_pos = get_position(self.s, self.s[0][-1])
        lst_pos = self.lst_pos()
        # 1. Fall: 4 ist über der 3 und beide werden zusammen 'reinrotiert' -> fertig
        if all(lst_pos == np.array(final_lst_pos) + d):
            pa = PosAction((0, len(self.s[0]) - 2), [r, d])
            locked = self.locked.union({self.lst_pos()})
            self.exec_pa(pa, locked)
        # 2. Fall: 3 und 4 sind vertauscht -> Überführung in 3. Fall
        elif all(lst_pos == np.array(final_lst_pos) + l):
            pa = PosAction((1, len(self.s[0]) - 2), [u])
            self.exec_pa(pa, self.locked)
            self.solve_last()
        # 3. Fall: Überführung in 1. Fall
        elif (all(lst_pos == np.array(final_lst_pos) + (1, -1)) and
              all(empty_position(self.p) == np.array(final_lst_pos) + l)):
            pa = PosAction(empty_position(self.p), [r, d, d, l, u, u, r, d, l,
                                                    u, r, d, d, l, u, r, d])
            self.exec_pa(pa, set())
            self.solve_last()
        # 4. Fall (default): Die 4 ist irgendwo anders -> Überführung in 1.
        else:
            self.p, acts = move_one_tile(self.p, self.s[0][-1],
                                         tuple(np.array(final_lst_pos) + d), self.locked)
            self._moves += acts
            self.solve_last()


    def execute(self):
        self.solve_but_last()
        self.solve_last()
        if self.transposed:
            return self.p.transpose(), [transpose_action(m) for m in self._moves]
        else:
            return self.p, self._moves


def next_is_column(p):
    """gibt an ob als nächstes eine spalte gelöst werden soll"""
    return p.shape[0] < p.shape[1] # es gibt mehr Spalten als Zeilen


def solve(p):
    counter = 0
    moves = []
    while not is_solved(p):
        log.info("solve, iteration {}, puzzle:\n{}".format(counter, p))
        counter += 1
        transp = next_is_column(p)
        ss = SolverStruct(p, moves, transp)
        p, moves = ss.execute()
        log.info("another row solved:\n{}".format(p))
        p = p[:, 1:] if transp else p[1:, :]
        log.info("shrinking p:\n{}".format(p))
        log.info("solved: " + str(is_solved(p)))
    return moves
