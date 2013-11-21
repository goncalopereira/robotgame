#!/usr/bin/env python

import os
import ast
import argparse
###
import game
import render
from settings import settings

parser = argparse.ArgumentParser(description="Robot game execution script.")
parser.add_argument("usercode1",
                    help="File containing first robot class definition.")
parser.add_argument("usercode2",
                    help="File containing second robot class definition.")
parser.add_argument("-m", "--map", help="User-specified map file.",
                    default='maps/default.py')
parser.add_argument("-H", "--headless", action="store_true",
                    default=False,
                    help="Disable rendering game output.")
parser.add_argument("-c", "--count", type=int,
                    default=1,
                    help="Game count, default: 1")

args = parser.parse_args()

def make_player(fname):
    return game.Player(open(fname).read())

def play(players, print_info=True):
    g = game.Game(*players, record_turns=True)
    for i in xrange(settings.max_turns):
        if print_info:
            print (' running turn %d ' % (g.turns + 1)).center(70, '-')
        g.run_turn()

    if print_info:
        render.Render(g, game.settings)
        print g.history

    return g.get_scores()

if __name__ == '__main__':

    map_name = os.path.join(args.map)
    map_data = ast.literal_eval(open(map_name).read())
    game.init_settings(map_data)

    players = [game.Player(open(args.usercode1).read()),
               game.Player(open(args.usercode2).read())]

    scores = []

    for i in xrange(args.count):
        scores.append(play(players, not args.headless))
        print scores[-1]

    if args.count > 1:
        p1won = reduce(lambda x, y: x + 1 if y[0] > y[1] else x,
                       scores, 0)
        p2won = reduce(lambda x, y: x + 1 if y[0] < y[1] else x,
                       scores, 0)
        print [p1won, p2won, args.count - p1won - p2won]
