import tkinter as tk
from tkinter import messagebox


# gui.py
class GUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Go Game")

        self.canvas = tk.Canvas(self.root, width=450, height=450, bg='sandybrown')
        self.canvas.pack()

        self.pass_button = tk.Button(self.root, text="Pass", command=self.game.pass_turn)
        self.pass_button.pack(side=tk.BOTTOM)

        self.move_history_label = tk.Label(self.root, text="Move History", font=('Arial', 12))
        self.move_history_label.pack(side=tk.RIGHT)

        self.history_box = tk.Text(self.root, width=20, height=15, font=('Arial', 10))
        self.history_box.pack(side=tk.RIGHT)

        self.score_label = tk.Label(self.root, text="Black: 0  White: 0", font=('Arial', 14))
        self.score_label.pack(side=tk.BOTTOM)

        self.last_move_id = None  # ID последнего выделенного хода

    def draw_board(self):
        cell_size = 450 // self.game.board.size
        self.canvas.delete("all")

        for i in range(self.game.board.size):
            self.canvas.create_line(cell_size * i + cell_size // 2, cell_size // 2, cell_size * i + cell_size // 2,
                                    450 - cell_size // 2)
            self.canvas.create_line(cell_size // 2, cell_size * i + cell_size // 2, 450 - cell_size // 2,
                                    cell_size * i + cell_size // 2)

        for x in range(self.game.board.size):
            for y in range(self.game.board.size):
                if self.game.board.grid[x][y] == 'B':
                    self.draw_stone(x, y, 'black')
                elif self.game.board.grid[x][y] == 'W':
                    self.draw_stone(x, y, 'white')

        self.update_score()

    def draw_stone(self, x, y, color):
        cell_size = 450 // self.game.board.size
        self.canvas.create_oval(cell_size * x + cell_size // 4, cell_size * y + cell_size // 4,
                                cell_size * x + 3 * cell_size // 4, cell_size * y + 3 * cell_size // 4, fill=color)

    def highlight_last_move(self, x, y):
        """Добавляем обводку вокруг последнего хода"""
        cell_size = 450 // self.game.board.size

        # Удаляем предыдущий индикатор, если он был
        if self.last_move_id is not None:
            self.canvas.delete(self.last_move_id)

        # Добавляем обводку вокруг клетки с последним ходом
        self.last_move_id = self.canvas.create_oval(cell_size * x + cell_size // 8,
                                                    cell_size * y + cell_size // 8,
                                                    cell_size * x + 7 * cell_size // 8,
                                                    cell_size * y + 7 * cell_size // 8,
                                                    outline="red", width=2)

    def update_score(self):
        black_score, white_score = self.game.board.count_points()
        self.score_label.config(text=f"Black: {black_score}  White: {white_score}")

    def update_move_history(self, move_history):
        self.history_box.delete(1.0, tk.END)
        for move in move_history:
            self.history_box.insert(tk.END, f"{move}\n")
        self.history_box.see(tk.END)

    @staticmethod
    def play():
        tk.mainloop()
