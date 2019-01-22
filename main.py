#!/usr/bin/env python

import argparse
import sys

from christmas.game import Game


WIDTH, HEIGHT = 700, 800


def main():
    # Parse optional debug flag.
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', action='store_true', help='Sets debugging flag.')
    args = vars(ap.parse_args())

    Game(WIDTH, HEIGHT, debug_mode=args['debug']).start()

if __name__ == '__main__':
    main()