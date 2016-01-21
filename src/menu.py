#!/usr/bin/env python3
import sys
import logging
import time
from sys import argv
import shell_utils as util
import puzzle as puz
import numpy as np
import solver_human_like as shl
import solvers



### constants ###

WELCOME_MESSAGE = """
Welcome to the 15 Puzzle!

Your Options:
(d) demo
(n) start a new game
(c) custom game
(q) quit
""".strip()


ACTION_NAMES = {(0, -1): ("a", "left"),
                (-1, 0): ("w", "up"),
                (0, +1): ("d", "right"),
                (+1, 0): ("s", "down")}


KEY_ACTIONS = dict([(k, a) for a, (k, _) in ACTION_NAMES.items()])


### string conversion ###

def str_dict(puzzle):
    d = dict()
    for elem in puzzle.flat:
        if elem == 0:
            d.update({elem: "."})
        else:
            d.update({elem: str(elem)})
    return d


def puzzle_to_str(puzzle):
    d = str_dict(puzzle)
    w = len(max(d.values(), key=len))
    strs = [d[e].rjust(w) for e in puzzle.flat]
    a = puz.from_list(strs, puzzle.shape)
    lines = [" ".join(l) for l in a]
    return "\n".join(lines)


### demo ###

def demo_path(puzzle, path):
    print("Enter speed (ms):")
    ms = util.read_number()
    sleep_time = ms / 1000
    print(puzzle_to_str(puzzle))
    path_len = len(path)
    while path:
        if sleep_time < 0:
            util.hit_enter()
        else:
            time.sleep(sleep_time)
        util.clear_screen()
        puzzle = puz.apply_action(puzzle, path[0])
        path = path[1:]
        print(puzzle_to_str(puzzle))
        print()
        print(path_len - len(path), "/", path_len)
        solved_tiles = puz.solved_tiles(puzzle)
        print(len(solved_tiles), solved_tiles)
        

def create_puzzle_with_dims():
    util.clear_screen()
    print("Enter Dimensions")
    print("rows:")
    n = util.read_number()
    print("cols:")
    m = util.read_number()
    p = puz.random_puzzle((n, m))
    return p


def demo_solver(p, solver_fn):
    start_time = time.time()
    path = solver_fn(p)
    exec_time = time.time() - start_time
    print("Time to find path:", exec_time, "seconds")
    print("Path length:      ", len(path))
    demo_path(p, path)


choose_solver_msg = """
Choose a method for solving
(a) IDA* 
(r) recursive IDA*
(h) human like
""".strip()
    

def choose_solver():
    print(choose_solver_msg)
    char = util.read_prompt()
    while True:
        if char == "a":
            return solvers.ida_star
        if char == "r":
            return solvers.rec_a_star
        if char == "h":
            return shl.solve
        print("Invalid Choice")


def main(filename = None):
    logging.getLogger().setLevel(logging.FATAL) # deactive logging
    if filename:
        p = puz.read_puzzle(filename)
    else:
        p = create_puzzle_with_dims()
    print(p)
    if not puz.solvable(p):
        print("Not solvable")
        return
    s = choose_solver()
    demo_solver(p, s)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(argv[1])
    else:
        main()
