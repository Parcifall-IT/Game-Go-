from board import Board
from tkinter import messagebox
from player import HumanPlayer
from bot import Bot
from gui import GUI


class GoGame:
    def __init__(self, board_size=9):
        self.board = Board(board_size)
        self.gui = GUI(self)
        self.current_player = HumanPlayer('B')
        self.bot_player = Bot('W', 1)
        self.passes = {'B': 0, 'W': 0}

        self.gui.draw_board()
        # Инициализация клика для человеческого игрока
        self.current_player.make_move(self)

    def click_handler(self, event):
        cell_size = 450 // self.board.size
        x = event.x // cell_size
        y = event.y // cell_size

        if isinstance(self.current_player, HumanPlayer) and self.place_stone(x, y):
            # Сбросить счетчик пропусков для текущего игрока.
            self.passes[self.current_player.color] = 0

            # Переключаемся на бота.
            self.current_player = self.bot_player

            # Бот делает ход.
            if isinstance(self.current_player, Bot):
                if not any(self.get_valid_moves()):
                    # Если у бота нет допустимых ходов - он пропускает ход.
                    self.passes[self.bot_player.color] += 1
                else:
                    # Бот делает ход.
                    self.current_player.make_move(self)

            self.gui.draw_board()
            # Проверяем на окончание игры после хода бота.
            if all(p == 1 for p in self.passes.values()) or self.board.is_full():
                # Если оба игрока пропустили ход или доска полна.
                self.end_game()
                return

            # Возвращаемся к человеку.
            self.current_player = HumanPlayer('B')

            # Обновляем доску после каждого хода.
            self.gui.draw_board()

    def place_stone(self, x, y):
        if self.board.place_stone(x, y, self.current_player):
            return True
        return False

    def pass_turn(self):
        # Пропускаем ход и проверяем конец игры.
        current_color = self.current_player.color

        # Увеличиваем счетчик пропусков для текущего игрока.
        if current_color == 'B':
            self.passes['B'] += 1
        else:
            self.passes['W'] += 1

        if all(p == 1 for p in self.passes.values()):
            # Если оба игрока пропустили ход - заканчиваем игру.
            messagebox.showinfo("Game Over", "Both players passed. Game over.")
            return True

        return False

    def get_valid_moves(self):
        valid_moves = []
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def end_game(self):
        black_score, white_score = self.board.count_score()

        messagebox.showinfo("Game Over", f"Final Scores:\nBlack: {black_score}\nWhite: {white_score}")

        if black_score > white_score:
            messagebox.showinfo("Game Over", "Black wins!")

        elif white_score > black_score:
            messagebox.showinfo("Game Over", "White wins!")

        else:
            messagebox.showinfo("Game Over", "It's a tie!")

        # Закрываем окно после окончания игры.
        self.gui.root.quit()

    def play(self):
        # Запускаем главный цикл приложения через GUI.
        self.gui.play()


if __name__ == "__main__":
    game = GoGame()
    game.play()
