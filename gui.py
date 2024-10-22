import tkinter as tk


class GUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Go Game")
        self.canvas = tk.Canvas(self.root, width=450, height=450, bg='sandybrown')
        self.canvas.pack()

    def draw_board(self):
        cell_size = 450 // self.game.board.size
        self.canvas.delete("all")

        # Рисуем сетку
        for i in range(self.game.board.size):
            self.canvas.create_line(cell_size * i + cell_size // 2,
                                    cell_size // 2,
                                    cell_size * i + cell_size // 2,
                                    450 - cell_size // 2)
            self.canvas.create_line(cell_size // 2,
                                    cell_size * i + cell_size // 2,
                                    450 - cell_size // 2,
                                    cell_size * i + cell_size // 2)

        # Рисуем камни
        for x in range(self.game.board.size):
            for y in range(self.game.board.size):
                if self.game.board.grid[x][y] == 'B':
                    self.draw_stone(x, y, 'black')
                elif self.game.board.grid[x][y] == 'W':
                    self.draw_stone(x, y, 'white')

    def draw_stone(self, x, y, color):
        cell_size = 450 // self.game.board.size
        self.canvas.create_oval(cell_size * x + cell_size // 4,
                                cell_size * y + cell_size // 4,
                                cell_size * x + 3 * cell_size // 4,
                                cell_size * y + 3 * cell_size // 4,
                                fill=color)

    @staticmethod
    def play():
        # Запускаем главный цикл приложения.
        tk.mainloop()