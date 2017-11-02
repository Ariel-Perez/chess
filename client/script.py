#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains the functionality to run custom scripts."""
from io import StringIO
from player import Player
from subprocess import check_output


class Script(Player):
    """Represents a single script for a chess engine."""

    def __init__(self, path):
        """Initialize a script."""
        self.path = path

    def play(self, board):
        """
        Play a move by calling the script.

        Return it in algebraic notation.
        """
        command = '%s "%s"' % (self.path, str(board))
        out = check_output(command.split(' '))
        return out
