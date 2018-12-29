#!/usr/bin/env python

import sys
import argparse

from christmas.game import Game

WIDTH, HEIGHT = 500, 800

def main():
    # Parse optional debug flag;w.
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', action='store_true', help='Sets debugging flag.')
    args = vars(ap.parse_args())

    Game(WIDTH, HEIGHT, debug_mode=args['debug']).start()

if __name__ == '__main__':
    main()