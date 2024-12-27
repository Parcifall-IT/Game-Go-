import unittest
from board import Board
from player import HumanPlayer as Player


class TestBoard(unittest.TestCase):
    def test_place_stone_valid_move(self):
        board = Board(size=5)
        player = Player('B')
        self.assertTrue(board.place_stone(2, 2, player))
        self.assertEqual(board.grid[2][2], 'B')

    def test_place_stone_invalid_move(self):
        board = Board(size=5)
        player = Player('B')
        board.grid[2][2] = 'W'
        self.assertFalse(board.place_stone(2, 2, player))
        self.assertEqual(board.grid[2][2], 'W')

    def test_is_on_board(self):
        board = Board(size=5)
        self.assertTrue(board.is_on_board(0, 0))
        self.assertTrue(board.is_on_board(4, 4))
        self.assertFalse(board.is_on_board(-1, 0))
        self.assertFalse(board.is_on_board(5, 5))

    def test_is_full(self):
        board = Board(size=3)
        board.grid = [
            ['B', 'W', 'B'],
            ['W', 'B', 'W'],
            ['B', 'W', 'B']
        ]
        self.assertTrue(board.is_full())

        board.grid[2][2] = '.'
        self.assertFalse(board.is_full())


if __name__ == "__main__":
    unittest.main()