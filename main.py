import random
import tkinter as tk
from tkinter import messagebox


class GoGame:
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'B'
        self.passes = 0
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Go Game")
        self.canvas = tk.Canvas(self.root, width=450, height=450, bg='sandybrown')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_handler)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 450 // self.board_size
        for i in range(self.board_size):
            self.canvas.create_line(cell_size * i + cell_size // 2, cell_size // 2,
                                    cell_size * i + cell_size // 2, 450 - cell_size // 2)
            self.canvas.create_line(cell_size // 2, cell_size * i + cell_size // 2,
                                    450 - cell_size // 2, cell_size * i + cell_size // 2)
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 'B':
                    self.draw_stone(x, y, 'black')
                elif self.board[x][y] == 'W':
                    self.draw_stone(x, y, 'white')

    def draw_stone(self, x, y, color):
        cell_size = 450 // self.board_size
        self.canvas.create_oval(cell_size * x + cell_size // 4, cell_size * y + cell_size // 4,
                                cell_size * x + 3 * cell_size // 4, cell_size * y + 3 * cell_size // 4,
                                fill=color, outline=color)

    def click_handler(self, event):
        cell_size = 450 // self.board_size
        x = event.x // cell_size
        y = event.y // cell_size
        if self.place_stone(x, y):
            self.draw_board()
            if self.current_player == 'W':
                self.computer_move()

    def is_on_board(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_valid_move(self, x, y):
        if not self.is_on_board(x, y) or self.board[x][y] != '.':
            return False
        # Here you should check for ko, suicide rules etc.
        return True

    def place_stone(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.passes = 0
            return True
        return False

    def pass_turn(self):
        self.passes += 1
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        if self.passes >= 1:
            self.end_game()

    def get_valid_moves(self):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def computer_move(self):
        valid_moves = self.get_valid_moves()
        if valid_moves:
            x, y = random.choice(valid_moves)
            self.place_stone(x, y)
            self.draw_board()
        else:
            self.pass_turn()

    def count_score(self):
        black_score = 0
        white_score = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 'B':
                    black_score += 1
                elif self.board[x][y] == 'W':
                    white_score += 1
                else:
                    if self.is_surrounded(x, y, 'B'):
                        black_score += 1
                    elif self.is_surrounded(x, y, 'W'):
                        white_score += 1
        return black_score, white_score

    def is_surrounded(self, x, y, player):
        to_check = [(x, y)]
        visited = set()
        while to_check:
            cx, cy = to_check.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                if self.is_on_board(nx, ny):
                    if self.board[nx][ny] == '.':
                        if not self.is_surrounded(nx, ny, player):
                            return False
                    elif self.board[nx][ny] != player:
                        return False
                    else:
                        to_check.append((nx, ny))
        return True

    def end_game(self):
        black_score, white_score = self.count_score()
        messagebox.showinfo("Game Over", f"Final Scores:\nBlack: {black_score}\nWhite: {white_score}")
        if black_score > white_score:
            messagebox.showinfo("Game Over", "Black wins!")
        elif white_score > black_score:
            messagebox.showinfo("Game Over", "White wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        self.root.quit()

    def play(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = GoGame()
    game.play()
