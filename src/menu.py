#!/usr/bin/env python3
from sys import argv
import util
import puzzle


WELCOME_MESSAGE = """
Welcome to the 15 Puzzle!

Your Options:
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


def custom_game():
    print("Enter Numbers separated by space")
    ns = util.read_prompt()
    ns = ns.split()
    ns = [int(n) for n in ns]
    p = puzzle.Puzzle(array=puzzle.list_to_array(ns))
    play(p)

            

def main():
    while True:
        util.clear_screen()
        print(WELCOME_MESSAGE)
        answer = util.read_prompt()
        if answer == "n":
            p = puzzle.Puzzle()
            p.shuffle()
            play(p)
        elif answer == "c":
            custom_game()
        elif answer == "q":
            exit(0)


if __name__ == "__main__":
    main()
