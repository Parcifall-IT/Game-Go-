class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    def is_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_valid_move(self, x, y, color):
        return self.is_on_board(x, y) and self.grid[x][y] == '.' and not self.is_suicide_move(x, y, color)

    def place_stone(self, x, y, player):
        if not self.is_valid_move(x, y, player.color):
            return False

        # Устанавливаем камень
        self.grid[x][y] = player.color
        opponent_color = 'W' if player.color == 'B' else 'B'

        # Удаляем захваченные камни противника, если они есть
        captured_any = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny) and self.grid[nx][ny] == opponent_color:
                if self.is_captured(nx, ny, opponent_color):
                    self.remove_captured_stones(nx, ny, opponent_color)
                    captured_any = True

        # Проверка на суицидальный ход после попытки захвата противника
        if not captured_any and self.is_captured(x, y, player.color):
            # Если ход суицидальный и не захватил камни противника, удаляем камень
            self.grid[x][y] = '.'
            return False

        return True

    def is_suicide_move(self, x, y, color):
        # Временная установка камня для проверки
        self.grid[x][y] = color
        opponent_color = 'W' if color == 'B' else 'B'

        # Проверяем, захватит ли ход хотя бы одну группу противника
        captures_opponent = any(
            self.is_captured(nx, ny, opponent_color)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if self.is_on_board(nx := x + dx, ny := y + dy) and self.grid[nx][ny] == opponent_color
        )

        # Проверяем, окружен ли наш камень, если он не захватывает камни противника
        is_suicide = not captures_opponent and self.is_captured(x, y, color)

        # Удаляем временно поставленный камень
        self.grid[x][y] = '.'
        return is_suicide

    def get_neighbors(self, x, y):
        """Возвращает список соседних координат для клетки (x, y)."""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def is_captured(self, x, y, color):
        # Проверка, окружена ли группа камней данного цвета
        stack = [(x, y)]
        group = set()
        visited = set()
        is_captured = True

        walls = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.add((cx, cy))

            for i, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                nx, ny = cx + dx, cy + dy
                if not self.is_on_board(nx, ny):
                    walls.add(i)
                    continue
                if self.grid[nx][ny] == '.':
                    is_captured = False  # Есть "дэмэ", значит группа не окружена
                elif self.grid[nx][ny] == color:
                    stack.append((nx, ny))

        if len(walls) >= 3:
            is_captured = False

        return is_captured

    def remove_captured_stones(self, x, y, color):
        # Удаление захваченной группы камней, только если у группы нет "дэмэ"
        if not self.is_captured(x, y, color):
            return 0

        # Собираем группу для удаления
        stack = [(x, y)]
        group = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in group:
                continue
            group.add((cx, cy))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if self.is_on_board(nx, ny) and self.grid[nx][ny] == color:
                    stack.append((nx, ny))

        # Удаление камней группы
        for cx, cy in group:
            self.grid[cx][cy] = '.'
        return len(group)

    def count_points(self):
        rows, cols = len(self.grid), len(self.grid[0])
        visited = [[False] * cols for _ in range(rows)]
        black_points = 0
        white_points = 0

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == 'B':
                    black_points += 1
                elif self.grid[i][j] == 'W':
                    white_points += 1

        def dfs(x, y):
            stack = [(x, y)]
            territory = set()
            color = None
            is_territory = True

            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy]:
                    continue
                visited[cx][cy] = True
                territory.add((cx, cy))

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if not self.is_on_board(nx, ny):
                        is_territory = False
                    elif self.grid[nx][ny] == '.':
                        if not visited[nx][ny]:
                            stack.append((nx, ny))
                    elif self.grid[nx][ny] in ['B', 'W']:
                        if color is None:
                            color = self.grid[nx][ny]
                        elif color != self.grid[nx][ny]:
                            is_territory = False
                            break

            return (territory, color) if is_territory else (set(), None)

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == '.' and not visited[i][j]:
                    territory, color = dfs(i, j)
                    if color == 'B':
                        black_points += len(territory)
                    elif color == 'W':
                        white_points += len(territory)

        return black_points, white_points

    def is_full(self):
        for row in self.grid:
            if '.' in row:
                return False
        return True
