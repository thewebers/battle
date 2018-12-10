#!/usr/bin/env python

import sys

from christmas.game import Game

WIDTH, HEIGHT = 500, 800

def main():
    Game(WIDTH, HEIGHT).start()

if __name__ == '__main__':
    main()