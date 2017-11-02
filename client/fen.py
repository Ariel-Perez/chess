#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This module contains functionality for the Forsyth-Edwards Notation."""
import re


class Fen:
    """Static class for dealing with the notation."""

    # Initial state in Forsyth-Edwards Notation (FEN)
    INITIAL_STATE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # Empty square notation for decompressed representation
    EMPTY_SQUARE = '-'

    def __init__(self, fen=None):
        if not fen:
            fen = Fen.INITIAL_STATE

        data = fen.split(" ")
        self.pieces = data[0]
        self.active = data[1]
        self.castling = data[2]
        self.en_passant = data[3]
        self.halfmove_clock = int(data[4])
        self.fullmove_number = int(data[5])

    def get_piece(self, col, row):
        """
        Get the piece at the given row and column.

        >>> f = Fen()
        >>> f.get_piece(0, 0)
        'R'
        >>> f.get_piece(0, 1)
        'P'
        >>> f.get_piece(4, 7)
        'k'
        >>> f.get_piece(4, 4)
        """
        rows = self.pieces.split('/')
        rows.reverse()

        row_pieces = Fen.decompress(rows[row])
        piece = row_pieces[col]
        return piece if piece != Fen.EMPTY_SQUARE else None

    def set_piece(self, col, row, piece):
        """
        Set a piece in a given row and column.

        >>> f = Fen()
        >>> f.set_piece(2, 3, 'B')
        >>> f.get_piece(2, 3)
        'B'
        >>> f.set_piece(0, 0, None)
        >>> f.get_piece(0, 0)
        """
        if piece is None:
            piece = Fen.EMPTY_SQUARE

        rows = self.pieces.split('/')
        rows.reverse()

        row_pieces = Fen.decompress(rows[row])
        row_pieces = row_pieces[:col] + piece + row_pieces[col + 1:]

        rows[row] = Fen.compress(row_pieces)
        rows.reverse()
        self.pieces = '/'.join(rows)

    @classmethod
    def compress(cls, piece_row):
        """
        Use numbers to compress the notation for pieces.

        >>> Fen.compress("--------")
        '8'
        >>> Fen.compress("p-P--Bq")
        'p1P2Bq'
        """
        pattern = '(%s+)' % Fen.EMPTY_SQUARE
        while True:
            match = re.search(pattern, piece_row)
            if match is None:
                break

            blanks = match.group(0)
            piece_row = piece_row.replace(blanks, str(len(blanks)), 1)

        return piece_row

    @classmethod
    def decompress(cls, piece_row):
        """
        Transform numbers to - in order to manipulate board pieces easily.

        >>> Fen.decompress('8')
        '--------'
        >>> Fen.decompress('p1P2Bq')
        'p-P--Bq'
        """
        pattern = r'([0-9])'
        while True:
            match = re.search(pattern, piece_row)
            if match is None:
                break

            num = match.group(0)
            piece_row = piece_row.replace(num, cls.EMPTY_SQUARE * int(num), 1)

        return piece_row

    def __str__(self):
        """
        Return the string representation of this FEN.

        >>> f = Fen()
        >>> str(f) == Fen.INITIAL_STATE
        True
        """
        fen = " ".join([
            self.pieces,
            self.active,
            self.castling,
            self.en_passant,
            str(self.halfmove_clock),
            str(self.fullmove_number)
        ])
        return fen

if __name__ == '__main__':
    import doctest
    doctest.testmod()
