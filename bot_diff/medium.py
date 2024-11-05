import random


def make_move(game):
    # Фильтруем валидные ходы, избегая самоубийственных
    valid_moves = [(x, y) for x, y in game.get_valid_moves() if game.board.is_valid_move(x, y, "W")]

    if valid_moves:
        x, y = random.choice(valid_moves)
        game.place_stone(x, y)
        game.gui.draw_board()  # Обновляем доску после хода бота
        return x, y  # Возвращаем координаты
    return None  # Если ходов нет, возвращаем None