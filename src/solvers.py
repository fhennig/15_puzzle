import math
import puzzle as puzzle
import util as u
import heapq as q
import collections as c

### heuristics ###

def manhattan_dist_sum(p):
    solved = puzzle.solved(p)
    s = 0
    for e in p.flat:
        s_pos = puzzle.get_position(p, e)
        t_pos = puzzle.get_position(solved, e)
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
        print("actions:", actions)
        print("hist:   ", self.hist)
#         if len(self.hist) > 0:
#             actions.remove(puzzle.reverse_action(self.hist[-1]))
        return actions


    def expand(self):
        return [Node(puzzle.apply_action(self.p, a),
                     self.hist + [a], self.heuristic)
                for a in self.useful_actions()]


    def is_goal(self):
        return puzzle.is_solved(self.p)

    
    def __lt__(self, other):
        return self.prio < other.prio
        


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
            stack.extend(nxt.expand())
    print(visited_nodes)
    if not found_goal:
        return None, next_bound
    else:
        return found_goal, None


def ida_star(p):
    node = Node(p, [], manhattan_dist_sum)
    bound = node.h_val
    while True:
        print(bound)
        goal, next_bound = bounded_dfs(node, bound)
        if not goal:
            bound = next_bound
        else:
            return goal.hist
        

# def binary_search(puzzle, min, max):
#     while max >= min:
#         mid = math.floor(min + ((max - min) / 2))
#         path = bounded_a_star(puzzle, mid)
#         if path:
#             max = mid
#         else:
#             min = mid
        