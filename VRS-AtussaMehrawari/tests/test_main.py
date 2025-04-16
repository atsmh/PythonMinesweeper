"""
Unittest code nach mypy-konformer Anpassung
"""

import unittest
import sys
import os
from typing import List, Union

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

from source.main import Board  # type: ignore  # mypy kennt source evtl. nicht beim Testen

class TestBoard(unittest.TestCase):

    def test_board_creation(self) -> None:
        board: Board = Board(dim_size=5, num_bombs=5)
        self.assertEqual(board.dim_size, 5)
        self.assertEqual(board.num_bombs, 5)
        self.assertEqual(len(board.board), 5)
        self.assertTrue(all(len(row) == 5 for row in board.board))

    def test_bomb_count(self) -> None:
        board: Board = Board(dim_size=5, num_bombs=5)
        bomb_count: int = sum(row.count('*') for row in board.board)
        self.assertEqual(bomb_count, 5)

    def test_dig_returns_false_on_bomb(self) -> None:
        board: Board = Board(dim_size=3, num_bombs=1)
        board.board = [[0, 0, 0], [0, '*', 0], [0, 0, 0]]  # type: ignore[assignment]
        board.assign_values_to_board()
        result: bool = board.dig(1, 1)
        self.assertFalse(result)

    def test_dig_returns_true_on_safe(self) -> None:
        board: Board = Board(dim_size=3, num_bombs=1)
        board.board = [[0, 0, 0], [0, '*', 0], [0, 0, 0]]  # type: ignore
        board.assign_values_to_board()
        result: bool = board.dig(0, 0)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
