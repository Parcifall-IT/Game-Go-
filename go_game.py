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

        # Проверяем, если ход человека, а не бота
        if isinstance(self.current_player, HumanPlayer) and self.place_stone(x, y):
            # Ход выполнен успешно, добавляем его в историю
            self.move_count += 1
            self.move_history.append(f"{self.move_count}. black ({x}, {y})")
            self.gui.update_move_history(self.move_history)

            # Рисуем доску с новым ходом
            self.gui.draw_board()
            self.gui.highlight_last_move(x, y)

            # Передаем ход боту
            self.current_player = self.bot_player

            # Обрабатываем ход бота
            if isinstance(self.current_player, Bot):
                # Проверяем, есть ли у бота доступные ходы
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

            # Обновляем счет и историю
            self.gui.update_score()
            self.gui.update_move_history(self.move_history)
            self.gui.update_passes(self.passes)

            # Проверяем окончание игры: либо доска заполнена, либо нет ходов у обоих игроков
            if self.board.is_full():
                self.end_game()
                return

            # Передаем ход обратно игроку
            self.current_player = HumanPlayer('B')

    def place_stone(self, x, y):
        if self.board.place_stone(x, y, self.current_player):
            return True
        return False

    def pass_turn(self):
        current_color = self.current_player.color

        # Проверка, остались ли пропуски у текущего игрока
        if self.passes[current_color] > 0:
            # Используем пропуск и обновляем счетчик
            self.passes[current_color] -= 1
            self.move_count += 1
            self.move_history.append(f"{self.move_count}. {current_color.lower()} passed")
            self.gui.update_move_history(self.move_history)
            self.gui.update_passes(self.passes)

            # Переключаем ход к сопернику
            if current_color == 'B':
                self.current_player = self.bot_player
            else:
                self.current_player = HumanPlayer('B')

            # Если ход переходит к боту, проверяем его доступные ходы
            if isinstance(self.current_player, Bot):
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    # Если есть ходы, бот делает ход
                    bot_move = self.current_player.make_move(self)
                    if bot_move:
                        bot_x, bot_y = bot_move
                        self.move_count += 1
                        self.move_history.append(f"{self.move_count}. white ({bot_x}, {bot_y})")
                        self.gui.update_move_history(self.move_history)
                        self.gui.draw_board()
                        self.gui.highlight_last_move(bot_x, bot_y)
                else:
                    # У бота нет ходов и нет пропусков, игра завершается
                    if self.passes['W'] == 0:
                        messagebox.showinfo("Game Over", "White has no moves and no passes left. Game over.")
                        self.end_game()
                        return

                # Возвращаем ход игроку после хода бота
                self.current_player = HumanPlayer('B')


        else:
            # Если у текущего игрока нет пропусков и нет ходов, игра завершается
            if not any(self.get_valid_moves()):
                messagebox.showinfo("Game Over",
                                    f"No moves left for {current_color} and no passes available. Game over.")
                self.end_game()
                return True

        # Обновляем пропуски после хода
        self.gui.update_passes(self.passes)
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
