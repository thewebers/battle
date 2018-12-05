#!/usr/bin/env python

import sys

from christmas.game import Game

WIDTH, HEIGHT = 320, 240

def main():
    Game(WIDTH, HEIGHT).start()

if __name__ == '__main__':
    main()
