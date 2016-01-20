#!/usr/bin/env python3
import sys
import logging
import time
from sys import argv
import shell_utils as util
import puzzle as puz
import numpy as np
import solver_human_like as shl


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


def play(p):
    moves = 0
    while True:
        util.clear_screen()
        print(p)
        print("Your Options:")
        opts = p.possible_actions()
        for opt in opts:
            key, desc = ACTION_NAMES[opt]
            print("(" + key + ")" + " " + desc)
        print("(q) quit"), print()
        print("moves:    ", moves)
        print("solvable: ", p.solvable())
        print("solved:   ", p.solved())
        action = util.read_prompt()
        if action == "q":
            break;
        if action in KEY_ACTIONS and KEY_ACTIONS[action] in opts:
            p = p.apply_action(KEY_ACTIONS[action])
            moves += 1


def custom_game(): ## TODO try catch
    print("Enter Numbers separated by space")
    ns = util.read_prompt()
    ns = ns.split()
    dim = len(puzzle.list_to_array(ns))
    d = util.invert_dict(puzzle.Puzzle(dim=dim).str_dict())
    ns = [d[n] for n in ns]
    p = puzzle.Puzzle(array=puzzle.list_to_array(ns))
    play(p)


def read_number():
    n = False
    while not n:
        s = util.read_prompt()
        try:
            n = int(s) # Kann einen Fehler ergeben
        except:
            pass
    return n


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


def demo_path(puzzle, path):
    print("Enter Speed:")
    ms = read_number()
    sleep_time = ms / 1000
    print(puzzle_to_str(puzzle))
    path_len = len(path)
    while path:
        puzzle = puz.apply_action(puzzle, path[0])
        path = path[1:]
        time.sleep(sleep_time)
        util.clear_screen()
        print(puzzle_to_str(puzzle))
        print()
        print(path_len - len(path), "/", path_len)
        solved_tiles = puz.solved_tiles(puzzle)
        print(len(solved_tiles), solved_tiles)
        

def demo():
    util.clear_screen()
    print("Enter Dimensions")
    print("rows:")
    n = read_number()
    print("cols:")
    m = read_number()
    p = puz.random_puzzle((n, m))
    demo_solver(p)


def demo_solver(p):
    print(p)
    start_time = time.time()
    path = shl.solve(p)
    exec_time = time.time() - start_time
    print("Time to find path:", exec_time, "seconds")
    print("Path length:      ", len(path))
    demo_path(p, path)


def read_puzzle(filename):
    with open(filename) as f:
        lines = f.read().strip().split("\n")
        nr_strs = [line.split(" ") for line in lines]
        nrs = [[int(s) for s in line] for line in nr_strs]
        puzzle = np.array(nrs)
        return puzzle
            

def main(filename = None):
    logging.getLogger().setLevel(logging.FATAL) ## deactive logging
    if filename:
        p = read_puzzle(filename)
        demo_solver(p)
    else:
        while True:
            util.clear_screen()
            print(WELCOME_MESSAGE)
            answer = util.read_prompt()
            if answer == "d":
                demo()
            if answer == "n":
                p = puzzle.Puzzle()
                p.shuffle()
                play(p)
            elif answer == "c":
                custom_game()
            elif answer == "q":
                exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(argv[1])
    else:
        main()
