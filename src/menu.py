#!/usr/bin/env python3
from sys import argv
import util
from puzzle import Puzzle


WELCOME_MESSAGE = """
Welcome to the 15 Puzzle!

Your Options:
(n) start a new game
(q) quit
""".strip()


ACTION_NAMES = {(0, -1): ("a", "left"),
                (-1, 0): ("w", "up"),
                (0, +1): ("d", "right"),
                (+1, 0): ("s", "down")}


KEY_ACTIONS = dict([(k, a) for a, (k, _) in ACTION_NAMES.items()])



def play(puzzle):
    p = puzzle
    while True:
        util.clear_screen()
        print(p)
        print("Your Options:")
        opts = p.possible_actions()
        for opt in opts:
            key, desc = ACTION_NAMES[opt]
            print("(" + key + ")" + " " + desc)
        print("(q) quit")
        print()
        action = util.read_prompt()
        if action == "q":
            break;
        if action in KEY_ACTIONS and KEY_ACTIONS[action] in opts:
            p.apply_action(KEY_ACTIONS[action])

            

def main():
    while True:
        util.clear_screen()
        print(WELCOME_MESSAGE)
        answer = util.read_prompt()
        if answer == "n":
            play(Puzzle(4))
        if answer == "q":
            exit(0)


if __name__ == "__main__":
    main()
