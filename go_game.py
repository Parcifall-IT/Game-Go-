from board import Board
from tkinter import messagebox, simpledialog
from player import HumanPlayer
from bot import Bot
from gui import GUI
from db.main import update_score


class GoGame:
    def __init__(self, parent, board_size=9, difficulty=1, on_game_end_callback=None, two_player_mode=False):
        self.board = Board(board_size)
        self.gui = GUI(parent, self, self.end_game)
        self.current_player = HumanPlayer('B')
        self.bot_player = Bot('W', difficulty) if not two_player_mode else HumanPlayer('W')
        self.two_player_mode = two_player_mode
        self.passes = {'B': 10, 'W': 2}  # Initialize skips to 2 per player
        self.move_history = []
        self.move_count = 0
        self.on_game_end_callback = on_game_end_callback

        self.gui.draw_board()
        self.gui.update_passes(self.passes)  # Display initial skip counters
        self.current_player.make_move(self)

    def click_handler(self, event):
        cell_size = 450 // self.board.size
        x = event.x // cell_size
        y = event.y // cell_size

        # Проверяем, если ход человека
        if isinstance(self.current_player, HumanPlayer) and self.place_stone(x, y):
            # Ход выполнен успешно, добавляем его в историю
            self.move_count += 1
            color = "black" if self.current_player.color == 'B' else "white"
            self.move_history.append(f"{self.move_count}. {color} ({x}, {y})")
            self.gui.update_move_history(self.move_history)

            # Рисуем доску с новым ходом
            self.gui.draw_board()
            self.gui.highlight_last_move(x, y)

            # Проверяем окончание игры
            if self.board.is_full():
                self.end_game()
                return

            # Переключаем ход
            if self.two_player_mode:
                self.current_player = HumanPlayer('W') if self.current_player.color == 'B' else HumanPlayer('B')
            else:
                self.current_player = self.bot_player if self.current_player.color == 'B' else HumanPlayer('B')

            # Если ход переходит к боту
            if isinstance(self.current_player, Bot):
                self.bot_move()

    def bot_move(self):
        # Ход бота
        if not any(self.get_valid_moves()):
            self.pass_turn()
        else:
            bot_move = self.current_player.make_move(self)
            if bot_move:
                bot_x, bot_y = bot_move
                self.move_count += 1
                self.move_history.append(f"{self.move_count}. white ({bot_x}, {bot_y})")
                self.gui.draw_board()
                self.gui.highlight_last_move(bot_x, bot_y)

            # Передаем ход обратно игроку
            self.current_player = HumanPlayer('B')

    def place_stone(self, x, y):
        if self.board.place_stone(x, y, self.current_player):
            return True
        return False

    def pass_turn(self):
        current_color = self.current_player.color

        if self.passes[current_color] > 0:
            self.passes[current_color] -= 1
            self.move_count += 1
            self.move_history.append(f"{self.move_count}. {current_color.lower()} passed")
            self.gui.update_move_history(self.move_history)
            self.gui.update_passes(self.passes)

            # Переключаем ход
            if self.two_player_mode:
                self.current_player = HumanPlayer('W') if self.current_player.color == 'B' else HumanPlayer('B')
            else:
                self.current_player = self.bot_player if self.current_player.color == 'B' else HumanPlayer('B')

            # Если ход переходит к боту
            if isinstance(self.current_player, Bot):
                self.bot_move()
        else:
            if not any(self.get_valid_moves()):
                messagebox.showinfo("Game Over", f"No moves left for {current_color} and no passes available. Game over.")
                self.end_game()

        self.gui.update_passes(self.passes)

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
