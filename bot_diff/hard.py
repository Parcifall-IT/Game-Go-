def make_move(game):
    best_move = calculate_move(game)
    # Совершаем наилучший найденный ход
    print(best_move)
    if best_move:
        game.place_stone(*best_move)
        game.gui.draw_board()
        return best_move
    return None


def calculate_move(game):
    # Получаем все допустимые ходы
    valid_moves = [(x, y) for x, y in game.get_valid_moves()
                   if game.board.is_valid_move(x, y, game.bot_player.color)]

    best_move = None
    best_score = -float('inf')

    # Оцениваем каждый возможный ход
    for move in valid_moves:
        x, y = move

        # 1. Захват территории
        territory_score = evaluate_territory(game, x, y)

        # 2. Атака на слабые группы противника
        attack_score = evaluate_attack(game, x, y)

        # 3. Защита собственных камней
        defense_score = evaluate_defense(game, x, y)

        # Общий эвристический счет для хода
        move_score = territory_score + attack_score + defense_score

        if move_score > best_score:
            best_score = move_score
            best_move = (x, y)

    return best_move


def evaluate_territory(game, x, y):
    # Предпочтение ходам рядом с пустыми областями для захвата территории
    territory_score = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if game.board.is_on_board(nx, ny) and game.board.grid[nx][ny] == '.':
            territory_score += 1
    return territory_score


def evaluate_attack(game, x, y):
    # Предпочтение ходам, которые могут захватить или окружить группы противника
    attack_score = 0
    opponent_color = 'B' if game.bot_player.color == 'W' else 'W'
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if game.board.is_on_board(nx, ny) and game.board.grid[nx][ny] == opponent_color:
            liberties = count_liberties(game, nx, ny)
            if liberties == 1:  # Если у группы противника одна свобода, атака приоритетнее
                attack_score += 5
            elif liberties == 2:
                attack_score += 2
    return attack_score


def evaluate_defense(game, x, y):
    # Предпочтение ходам, которые увеличивают свободы собственной группы
    defense_score = 0
    color = game.bot_player.color
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if game.board.is_on_board(nx, ny) and game.board.grid[nx][ny] == color:
            liberties = count_liberties(game, nx, ny)
            defense_score += liberties  # Защищаем группы с низкими свободами
    return defense_score


def count_liberties(game, x, y):
    # Подсчет свобод (пустых соседних клеток) для камня или группы на позиции (x, y)
    color = game.board.grid[x][y]
    visited = set()
    stack = [(x, y)]
    liberties = 0

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if game.board.is_on_board(nx, ny):
                if game.board.grid[nx][ny] == '.':
                    liberties += 1
                elif game.board.grid[nx][ny] == color and (nx, ny) not in visited:
                    stack.append((nx, ny))

    return liberties
