#!/usr/bin/env python

import sys

from engine import GameEngine

def main():
    if len(sys.argv) == 2:
        width, height = [int(x) for x in sys.argv] 
        GameEngine(width, height).start()
    GameEngine().start()

if __name__ == '__main__':
    main()