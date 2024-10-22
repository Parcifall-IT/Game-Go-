import random


def make_move(game):
    valid_moves = game.get_valid_moves()
    if valid_moves:
        x, y = random.choice(valid_moves)
        game.place_stone(x, y)
        game.gui.draw_board()  # Обновляем доску после хода бота