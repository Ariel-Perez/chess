#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains all game functionality."""
import argparse
from board import Board
from script import Script
from human import Human


class Game:
    """
    Game controller.

    This class will either allow users to play or
    make calls to the engine scripts, depending on configuration.
    """

    def __init__(self, white, black):
        """Initialize the Game."""
        self.board = Board()
        self.white = Script(white) if white else Human("White")
        self.black = Script(black) if black else Human("Black")

    def update(self, move):
        """Update the internal variables from the state."""
        self.board.update(move)

    def play(self, player):
        """Get a move from the given player and update the board."""
        move = player.play(self.board)
        self.board.update(move)
        # TODO: Display this in a more decent way
        print(move, str(self.board))

    def loop(self):
        while True:
            # TODO: Validate moves and detect victory
            self.play(self.white)
            self.play(self.black)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--white", help="Script to play as white")
    parser.add_argument("-b", "--black", help="Script to play as black")
    args = parser.parse_args()
    game = Game(args.white, args.black)
    game.loop()
