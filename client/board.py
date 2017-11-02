#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains all board functionality."""
import re
from fen import Fen


class Board:
    """This class will keep an internal representation of the game."""

    def __init__(self, state=None):
        """Initialize the Game."""
        self.state = Fen(state)

    def get_indices(self, location):
        """
        Get the col and row indices for a location.

        >>> b = Board()
        >>> b.get_indices('a2')
        (0, 1)
        >>> b.get_indices('h7')
        (7, 6)
        """
        row = int(location[1]) - 1
        col = ord(location[0]) - ord('a')
        return col, row

    def get_piece(self, location):
        """
        Get the piece in a given location.

        >>> b = Board()
        >>> b.get_piece('e1')
        'K'
        >>> b.get_piece('f8')
        'b'
        """
        col, row = self.get_indices(location)
        return self.state.get_piece(col, row)

    def set_piece(self, location, piece):
        """
        Set a piece in a given location.

        >>> b = Board()
        >>> b.set_piece('d5', 'B')
        >>> b.get_piece('d5')
        'B'
        """
        col, row = self.get_indices(location)
        self.state.set_piece(col, row, piece)

    def update(self, move):
        """
        Update the internal variables from the state.

        >>> b = Board()
        >>> b.update("e2e4")
        >>> str(b)
        'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
        >>> b.update("c7c5")
        >>> str(b)
        'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'
        >>> b.update("g1f3")
        >>> str(b)
        'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
        """
        start = move[:2]
        target = move[2:]

        piece = self.get_piece(start)
        target_piece = self.get_piece(target)

        # Perform the move
        self.set_piece(start, None)
        self.set_piece(target, piece)

        # Turn toggle + move counter
        self.state.active = 'b' if self.state.active == 'w' else 'w'
        if self.state.active == 'w':
            self.state.fullmove_number += 1

        # Castling
        if start in ('e1', 'h1'):
            self.state.castling.replace("K", "")
        if start in ('e1', 'a1'):
            self.state.castling.replace("Q", "")
        if start in ('e8', 'h8'):
            self.state.castling.replace("k", "")
        if start in ('e8', 'a8'):
            self.state.castling.replace("q", "")
        if self.state.castling == "":
            self.state.castling = "-"

        # Check whether there was a capture
        capture = target_piece is not None
        pawn_move = piece in ('p', 'P')
        # Count half-moves without captures or pawn movements
        self.state.halfmove_clock = (
            0 if capture or pawn_move
            else self.state.halfmove_clock + 1
        )

        # En passant
        col = start[0]
        start_row = int(start[1])
        target_row = int(target[1])
        if pawn_move and abs(target_row - start_row) == 2:
            self.state.en_passant = col + str(
                (start_row + target_row) // 2
            )
        else:
            self.state.en_passant = '-'

    def __str__(self):
        """
        Return the FEN representation of the board.

        >>> b = Board()
        >>> str(b) == Fen.INITIAL_STATE
        True
        """
        return str(self.state)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
