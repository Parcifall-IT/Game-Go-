from board import Board
from tkinter import messagebox, simpledialog
from player import HumanPlayer
from bot import Bot
from gui import GUI
from db.main import update_score


class GoGame:
    def __init__(self, parent, board_size=9, difficulty=1, on_game_end_callback=None):
        self.board = Board(board_size)
        self.gui = GUI(parent, self, self.end_game)
        self.current_player = HumanPlayer('B')
        self.bot_player = Bot('W', difficulty)
        self.passes = {'B': 0, 'W': 0}
        self.move_history = []
        self.move_count = 0
        self.on_game_end_callback = on_game_end_callback

        self.gui.draw_board()
        self.current_player.make_move(self)

    def click_handler(self, event):
        cell_size = 450 // self.board.size
        x = event.x // cell_size
        y = event.y // cell_size

        if isinstance(self.current_player, HumanPlayer) and self.place_stone(x, y):
            self.passes[self.current_player.color] = 0
            self.move_count += 1
            self.move_history.append(f"{self.move_count}. black ({x}, {y})")
            self.gui.update_move_history(self.move_history)

            self.gui.draw_board()
            self.gui.highlight_last_move(x, y)

            self.current_player = self.bot_player

            if isinstance(self.current_player, Bot):
                if not any(self.get_valid_moves()):
                    self.pass_turn()
                    self.passes[self.bot_player.color] += 1
                else:
                    bot_move = self.current_player.make_move(self)
                    if bot_move:
                        bot_x, bot_y = bot_move
                        self.move_count += 1
                        self.move_history.append(f"{self.move_count}. white ({bot_x}, {bot_y})")
                        self.gui.draw_board()
                        self.gui.highlight_last_move(bot_x, bot_y)

            self.gui.update_score()
            self.gui.update_move_history(self.move_history)

            if all(p == 1 for p in self.passes.values()) or self.board.is_full():
                self.end_game()
                return

            self.current_player = HumanPlayer('B')

    def place_stone(self, x, y):
        if self.board.place_stone(x, y, self.current_player):
            return True
        return False

    def pass_turn(self):
        current_color = self.current_player.color

        self.passes[current_color] += 1
        self.move_count += 1
        self.move_history.append(f"{self.move_count}. {current_color.lower()} passed")
        self.gui.update_move_history(self.move_history)

        bb = False

        if self.passes[current_color] >= 2:
            messagebox.showinfo("Game Over", f"{current_color} player passed twice. Game over.")
            self.end_game()
            return True

        if current_color == 'B':
            self.current_player = self.bot_player
            bot_move = self.current_player.make_move(self)

            if bot_move:
                bot_x, bot_y = bot_move
                bb = True
                self.move_count += 1
                self.move_history.append(f"{self.move_count}. white ({bot_x}, {bot_y})")

            else:
                self.passes['W'] += 1
                self.move_count += 1
                self.move_history.append(f"{self.move_count}. white passed")
                if self.passes['W'] >= 2:
                    messagebox.showinfo("Game Over", "White player passed twice. Game over.")
                    self.end_game()
                    return True

            self.current_player = HumanPlayer('B')

        else:
            self.current_player = HumanPlayer('B')

        if self.board.is_full():
            messagebox.showinfo("Game Over", "The board is full. Game over.")
            self.end_game()
            return True

        self.gui.update_move_history(self.move_history)
        self.gui.draw_board()
        if bb:
            self.gui.highlight_last_move(bot_x, bot_y)
        return False

    def get_valid_moves(self):
        return [(x, y) for x in range(self.board.size) for y in range(self.board.size)
                if self.board.is_valid_move(x, y, self.current_player.color)]

    def end_game(self):
        black_score, white_score = self.board.count_points()
        messagebox.showinfo("Game Over", f"Final Scores:\nBlack: {black_score}\nWhite: {white_score}")

        if black_score > white_score:
            messagebox.showinfo("Game Over", "Black wins!")
        elif white_score > black_score:
            messagebox.showinfo("Game Over", "White wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

        name = simpledialog.askstring(
            "Введите имя",
            "Введите своё имя для сохранения результата (или оставьте пустым, чтобы отказаться):")

        if name:
            update_score(name, black_score)

        if self.on_game_end_callback:
            self.on_game_end_callback()

    def play(self):
        self.gui.draw_board()