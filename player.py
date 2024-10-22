class HumanPlayer():
    def __init__(self, color):
        self.color = color

    @staticmethod
    def make_move(game):
        game.gui.canvas.bind("<Button-1>", game.click_handler)
