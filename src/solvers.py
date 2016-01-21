import math
import numpy as np
import puzzle as puzzle
import util as u
import heapq as q
import collections as c

### heuristics ###

def manhattan_dist_sum(p, tiles = None):
    if not tiles:
        tiles = p.flat
    solved = puzzle.solved(p)
    s = 0
    for t in tiles:
        s_pos = puzzle.get_position(p, t)
        t_pos = puzzle.get_position(solved, t)
        s += u.manhattan_distance(*s_pos, *t_pos)
    return s


### iterative deepening a star ###

class Node:
    def __init__(self, p, hist, heuristic):
        self.p = p
        self.hist = hist
        self.heuristic = heuristic
        self.prio = len(self.hist) + self.heuristic(self.p)
        self.h_val = self.prio


    def useful_actions(self):
        actions = puzzle.possible_actions(self.p)
        if len(self.hist) > 0:
             actions.remove(puzzle.reverse_action(self.hist[-1]))
        return actions


    def expand(self):
        return [Node(puzzle.apply_action(self.p, a),
                     self.hist + [a], self.heuristic)
                for a in self.useful_actions()]


    def is_goal(self):
        return self.heuristic(self.p) == 0

    
    def __lt__(self, other):
        return self.prio < other.prio

    
def a_star(puzzle, heuristic):
    """returns the shortest path to a state where heuristic(puzzle) == 0"""
    queue = []
    init_node = Node(puzzle, [], heuristic) ## TODO change heuristic
    q.heappush(queue, init_node)
    while queue:
        node = q.heappop(queue)
#        print(node.p)
#        print(node.prio, node.h_val)
        if heuristic(node.p) == 0:
            return node.hist
        for nxt in node.expand():
            q.heappush(queue, nxt)
    return None


# def bounded_a_star(puzzle, bound):
#     queue = []
#     init_node = Node(puzzle, [], manhattan_dist_sum)
#     q.heappush(queue, init_node)
#     while queue:
#         node = q.heappop(queue)
#         if len(node.hist) > bound:
#             continue
#         if node.puzzle.solved():
#             return node.hist
#         for nxt in node.expand():
#             if not nxt.prio > bound:
#                 q.heappush(queue, nxt)
#     return None


# def id_a_star(puzzle):
#     bound = manhattan_dist_sum(puzzle)
#     while True:
#         print(bound)
#         path = bounded_a_star(puzzle, bound)
#         if path:
#             return path
#         bound += 1


### iterative deepening A* ###

def bounded_dfs(node, bound):
    stack = [node]
    next_bound = 10**100
    visited_nodes = 0
    found_goal = None
    while stack:
        nxt = stack.pop()
        visited_nodes += 1
        if nxt.h_val > bound:
            next_bound = min(next_bound, nxt.h_val)
        elif nxt.is_goal():
            found_goal = nxt
            break
        else:
            l = sorted(nxt.expand(), key = lambda n: n.h_val, reverse = True)
            stack.extend(l)
#    print(visited_nodes)
    if not found_goal:
        return None, next_bound
    else:
        return found_goal, None


def ida_star(p, heuristic = manhattan_dist_sum):
    node = Node(p, [], heuristic)
    bound = node.h_val
    while True:
#        print(bound)
        goal, next_bound = bounded_dfs(node, bound)
        if not goal:
            bound = next_bound
        else:
#            print("path with len {} found: {}".format(len(goal.hist), goal.hist))
            return goal.hist


def binary_a_star(p, heuristic):
    node = Node(p, [], heuristic)
    min = node.h_val
    max = min * 2
    result = None
    while min != max:
        bound = min + math.floor((max - min) / 2)
#        print(bound, min, max)
        goal, next_bound = bounded_dfs(node, bound)
        if not goal:
            min = next_bound
            bound = next_bound
        else:
            max = bound
#            print("path with len {} found: {}".format(len(goal.hist), goal.hist))
            result = goal.hist
    return result
        

### recursive A* ###

class SubSelect:
    def __init__(self, n = 1):
        self.n = 1

    def applicable(self, p):
        return all(np.array(p.shape) > (self.n, ) * len(p.shape))
        
    def apply(self, p):
        return p[(slice(self.n, None),) * len(p.shape)]


def rec_a_star(p, selector = SubSelect()):
    solved = puzzle.solved(p)
    path = []
    while selector.applicable(p):
        tiles_to_solve = [t for t in solved.flat if t not in selector.apply(solved)]
        heuristic = lambda puz: manhattan_dist_sum(puz, tiles_to_solve)
        new_path = ida_star(p, heuristic)
        path += new_path
        p = selector.apply(puzzle.apply_actions(p, new_path))
        solved = selector.apply(solved)
    path += a_star(p, manhattan_dist_sum)
    return path
