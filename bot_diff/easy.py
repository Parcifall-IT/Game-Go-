import random
from bot_diff import hard


def make_move(game):
    valid_moves = [(x, y) for x, y in game.get_valid_moves()
                   if game.board.is_valid_move(x, y, "W") and not game.board.is_suicide_move(x, y, "W")]

    if valid_moves:
        x, y = random.choice(valid_moves)
        best_move = hard.make_move(game)
        while (x, y) == best_move:
            x, y = random.choice(valid_moves)
        game.place_stone(x, y)
        game.gui.draw_board()
        return x, y
    return None
