#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains the base player class."""
from abc import ABC, abstractmethod


class Player(ABC):
    """
    Abstract class for player functionality.

    This can be either a human or a script.
    """

    @abstractmethod
    def play(self, board):
        """Play a move and return it in algebraic notation."""
        ...
