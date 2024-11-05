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

        # Помещаем камень игрока на доску (симуляция)
        self.grid[x][y] = player.color

        # Проверяем, не является ли ход самоубийственным
        if self.is_suicide_move(x, y, player.color):
            self.grid[x][y] = '.'  # Откат хода
            return False

        # Удаляем захваченные группы противника вокруг
        opponent_color = 'W' if player.color == 'B' else 'B'
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny) and self.grid[nx][ny] == opponent_color:
                self.remove_captured_stones(nx, ny, opponent_color)

        return True

    def is_suicide_move(self, x, y, color):
        """Проверка, является ли ход самоубийственным."""
        # Проверяем, окружена ли группа после хода
        return self.is_captured(x, y, color)

    def is_captured(self, x, y, color):
        """Проверяет, будет ли группа камней, включая (x, y), захвачена, учитывая правила стен."""
        stack = [(x, y)]
        group = set()
        visited = set()
        opponent_color = 'W' if color == 'B' else 'B'
        wall_count = 0  # Счетчик сторон, соприкасающихся с границами доски
        is_captured = True

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.add((cx, cy))

            # Проверяем соседние клетки
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if not self.is_on_board(nx, ny):
                    # Если соседняя клетка за пределами доски, увеличиваем счетчик стен
                    wall_count += 1
                elif self.grid[nx][ny] == '.':
                    # Если рядом есть пустая клетка, группа не окружена
                    is_captured = False
                elif self.grid[nx][ny] == color:
                    # Если соседняя клетка того же цвета, добавляем её в стек для проверки
                    stack.append((nx, ny))
                elif self.grid[nx][ny] == opponent_color:
                    # Если клетка принадлежит противнику, продолжаем обход группы
                    continue

        # Если группа окружена, но соприкасается с тремя или более стенами, она не считается захваченной
        if wall_count >= 3:
            is_captured = False

        return is_captured

    def remove_captured_stones(self, x, y, color):
        """Удаляет захваченные камни группы заданного цвета, если группа окружена."""
        stack = [(x, y)]
        group = set()
        visited = set()
        is_captured = True

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.add((cx, cy))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if self.is_on_board(nx, ny):
                    if self.grid[nx][ny] == '.':
                        is_captured = False  # Группа не окружена, если есть пустая клетка
                    elif self.grid[nx][ny] == color:
                        stack.append((nx, ny))  # Продолжаем обход группы

        if is_captured:
            for cx, cy in group:
                self.grid[cx][cy] = '.'  # Удаляем захваченные камни
            return len(group)  # Возвращаем количество удаленных камней

        return 0  # Если группа не окружена, возвращаем 0

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
