import random


def make_move(game):
    # Находим наилучший ход по количеству очков и захвату территории
    best_move = None
    max_captured = 0
    for x, y in game.get_valid_moves():
        game.board.place_stone(x, y, game.current_player)
        captured_stones = game.board.remove_captured_stones(x, y, game.current_player.color)
        if captured_stones > max_captured:
            max_captured = captured_stones
            best_move = (x, y)
        game.board.grid[x][y] = '.'  # Откат хода после оценки

    # Если нашли лучший ход, делаем его
    if best_move:
        x, y = best_move
        game.place_stone(x, y)
        game.gui.draw_board()
    else:
        # Иначе выполняем случайный ход
        valid_moves = game.get_valid_moves()
        if valid_moves:
            x, y = random.choice(valid_moves)
            game.place_stone(x, y)
            game.gui.draw_board()
