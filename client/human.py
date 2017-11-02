#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains the base player class."""
from player import Player


class Human(Player):
    """Implementation of a human player"""

    def __init__(self, name):
        """Initialize the human player."""
        self.name = name

    def play(self, board):
        """Play a move and return it in algebraic notation."""
        move = input("%s move:" % self.name)
        return move
