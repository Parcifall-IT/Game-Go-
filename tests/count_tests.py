import unittest
from board import Board


class TestGoGameScoring(unittest.TestCase):
    def setUp(self):
        self.board = Board(9)

    def test_empty_board(self):
        black_score, white_score = self.board.count_points()
        self.assertEqual(black_score, 0)
        self.assertEqual(white_score, 0)

    def test_stone_counting(self):
        # Добавляем несколько камней на доску
        self.board.grid[0][0] = 'B'
        self.board.grid[0][1] = 'W'
        self.board.grid[1][0] = 'B'
        self.board.grid[1][1] = 'W'
        black_score, white_score = self.board.count_points()
        self.assertEqual(black_score, 2)
        self.assertEqual(white_score, 2)

    def test_surrounded_territory(self):
        # Окружаем пустую зону черными камнями
        self.board.grid[2][2] = 'B'
        self.board.grid[2][3] = 'B'
        self.board.grid[2][4] = 'B'
        self.board.grid[3][2] = 'B'
        self.board.grid[3][4] = 'B'
        self.board.grid[4][2] = 'B'
        self.board.grid[4][3] = 'B'
        self.board.grid[4][4] = 'B'
        black_score, white_score = self.board.count_points()
        self.assertEqual(black_score, 9)  # 8 камней + 1 окруженная пустая клетка
        self.assertEqual(white_score, 0)

    def test_mixed_territory(self):
        # Окруженная пустая зона, но с камнями обоих цветов вокруг
        self.board.grid[2][2] = 'B'
        self.board.grid[2][3] = 'W'
        self.board.grid[3][2] = 'W'
        self.board.grid[3][3] = 'B'
        black_score, white_score = self.board.count_points()
        self.assertEqual(black_score, 2)  # только за камни, т.к. территория не принадлежит одному игроку
        self.assertEqual(white_score, 2)

    def test_captured_stones(self):
        # Тестируем, что камни внутри чужой окруженной территории увеличивают очки
        self.board.grid[2][2] = 'B'
        self.board.grid[2][3] = 'B'
        self.board.grid[2][4] = 'B'
        self.board.grid[3][2] = 'B'
        self.board.grid[3][4] = 'B'
