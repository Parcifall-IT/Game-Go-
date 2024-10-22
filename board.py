class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    def is_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_valid_move(self, x, y):
        if not self.is_on_board(x, y) or self.grid[x][y] != '.':
            return False
        return True

    def place_stone(self, x, y, player):
        if self.is_valid_move(x, y):
            self.grid[x][y] = player.color
            return True
        return False

    def count_score(self):
        black_score = 0
        white_score = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 'B':
                    black_score += 1
                elif self.grid[x][y] == 'W':
                    white_score += 1
                else:
                    if self.is_surrounded(x, y, 'B'):
                        black_score += 1
                    elif self.is_surrounded(x, y, 'W'):
                        white_score += 1
        return black_score, white_score

    def is_surrounded(self, x, y, player):
        to_check = [(x, y)]
        visited = set()
        while to_check:
            cx, cy = to_check.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
                if self.is_on_board(nx, ny):
                    if self.grid[nx][ny] == '.':
                        if not self.is_surrounded(nx, ny, player):
                            return False
                    elif self.grid[nx][ny] != player:
                        return False
                    else:
                        to_check.append((nx, ny))
        return True

    def is_full(self):
        # Проверка на заполненность доски.
        for row in self.grid:
            if '.' in row:
                return False
        return True

