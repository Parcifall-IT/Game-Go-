from bot_diff import easy, medium, hard


class Bot:
    def __init__(self, color, difficulty):
        self.color = color
        self.difficulty = difficulty

    def make_move(self, game):
        return [easy, medium, hard][self.difficulty].make_move(game)
