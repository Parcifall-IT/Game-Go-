import tkinter as tk
from go_game import GoGame
from db.main import find_top_users


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Go Game")
        self.root.geometry("500x700")
        self.root.configure(bg="#F4A460")

        self.main_frame = tk.Frame(self.root, bg="#F4A460")
        self.main_frame.pack(fill="both", expand=True)

        # Default settings
        self.board_size = 9
        self.player_count = 1  # Default to single player

        self.show_main_menu()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    @staticmethod
    def style_button(button):
        button.configure(
            font=("Arial", 12, "bold"),
            bg="#D2691E",
            fg="white",
            activebackground="#8B4513",
            activeforeground="white",
            width=20,
            height=2,
            relief="flat",
            bd=0
        )

    def show_main_menu(self):
        self.clear_frame()

        title_label = tk.Label(
            self.main_frame,
            text="Go Game",
            font=("Consolas", 24, "bold"),
            fg="#8B4513",
            bg="#F4A460"
        )
        title_label.pack(pady=30)

        start_button = tk.Button(self.main_frame, text="Начать игру", command=self.show_difficulty_selection)
        self.style_button(start_button)
        start_button.pack(pady=10)

        leaderboard_button = tk.Button(self.main_frame, text="Таблица лидеров", command=self.show_leaderboard)
        self.style_button(leaderboard_button)
        leaderboard_button.pack(pady=10)

        settings_button = tk.Button(self.main_frame, text="Настройки", command=self.show_settings)
        self.style_button(settings_button)
        settings_button.pack(pady=10)

        exit_button = tk.Button(self.main_frame, text="Выход", command=self.root.quit)
        self.style_button(exit_button)
        exit_button.pack(pady=10)

    def show_difficulty_selection(self):
        self.clear_frame()

        label = tk.Label(
            self.main_frame,
            text="Выберите уровень сложности:",
            font=("Consolas", 16, "bold"),
            fg="#8B4513",
            bg="#F4A460"
        )
        label.pack(pady=20)

        for level, text in enumerate(["Легко", "Средне", "Трудно"]):
            button = tk.Button(self.main_frame, text=text, command=lambda lvl=level: self.start_game(lvl))
            self.style_button(button)
            button.pack(pady=5)

        back_button = tk.Button(self.main_frame, text="Назад", command=self.show_main_menu)
        self.style_button(back_button)
        back_button.pack(pady=10)

    def show_leaderboard(self):
        self.clear_frame()

        label = tk.Label(
            self.main_frame,
            text="Таблица лидеров",
            font=("Consolas", 18, "bold"),
            fg="#8B4513",
            bg="#F4A460"
        )
        label.pack(pady=20)

        sample_text = ""
        for i, user in enumerate(find_top_users()):
            sample_text += f"{i + 1}. {user.name} " \
                           f"{'-' * (19 - len(user.name) - len(str(user.score)))} {user.score} очков\n"

        leaderboard_label = tk.Label(
            self.main_frame,
            text=sample_text,
            font=("Consolas", 14),
            fg="#8B4513",
            bg="#F4A460",
            justify='left'
        )
        leaderboard_label.pack(pady=20)

        back_button = tk.Button(self.main_frame, text="Назад", command=self.show_main_menu)
        self.style_button(back_button)
        back_button.pack(pady=10)

    def show_settings(self):
        self.clear_frame()

        label = tk.Label(
            self.main_frame,
            text="Настройки",
            font=("Consolas", 18, "bold"),
            fg="#8B4513",
            bg="#F4A460"
        )
        label.pack(pady=20)

        # Поле для ввода размера доски
        board_size_label = tk.Label(
            self.main_frame,
            text="Размер поля:",
            font=("Consolas", 14),
            fg="#8B4513",
            bg="#F4A460"
        )
        board_size_label.pack(pady=10)

        size_var = tk.StringVar(value=str(self.board_size))
        board_size_entry = tk.Entry(self.main_frame, textvariable=size_var, font=("Consolas", 14), justify='center')
        board_size_entry.pack(pady=10)

        # Выбор количества игроков
        player_count_label = tk.Label(
            self.main_frame,
            text="Количество игроков:",
            font=("Consolas", 14),
            fg="#8B4513",
            bg="#F4A460"
        )
        player_count_label.pack(pady=10)

        player_count_var = tk.IntVar(value=self.player_count)
        # Создаем общий контейнер для радиокнопок
        player_count_frame = tk.Frame(self.main_frame, bg="#F4A460")
        player_count_frame.pack()  # Выравнивание по левому краю

        # Радиокнопки для выбора количества игроков
        one_player_radio = tk.Radiobutton(
            player_count_frame,
            text="1 Игрок",
            variable=player_count_var,
            value=1,
            font=("Consolas", 12),
            fg="#8B4513",
            bg="#F4A460",
            activebackground="#F4A460",
            anchor="w",  # Выравнивание текста в самой кнопке
            justify="center"
        )
        one_player_radio.pack(anchor='w')  # Выравнивание кнопки в контейнере

        two_player_radio = tk.Radiobutton(
            player_count_frame,
            text="2 Игрока",
            variable=player_count_var,
            value=2,
            font=("Consolas", 12),
            fg="#8B4513",
            bg="#F4A460",
            activebackground="#F4A460",
            anchor="w",  # Выравнивание текста в самой кнопке
            justify="center"
        )
        two_player_radio.pack(anchor='w')  # Выравнивание кнопки в контейнере

        def save_settings():
            try:
                new_size = int(size_var.get())
                if new_size < 5 or new_size > 18:
                    raise ValueError("Размер должен быть от 5 до 18.")
                self.board_size = new_size
                self.player_count = player_count_var.get()
                self.show_main_menu()
            except ValueError as e:
                error_label.config(text=f"Ошибка: {e}")

        save_button = tk.Button(self.main_frame, text="Сохранить", command=save_settings)
        self.style_button(save_button)
        save_button.pack(pady=10)

        error_label = tk.Label(
            self.main_frame,
            text="",
            font=("Consolas", 12),
            fg="red",
            bg="#F4A460"
        )
        error_label.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="Назад", command=self.show_main_menu)
        self.style_button(back_button)
        back_button.pack(pady=10)

    def start_game(self, difficulty):
        self.clear_frame()

        # Передача параметра количества игроков в GoGame
        two_player_mode = self.player_count == 2
        game = GoGame(
            parent=self.main_frame,
            difficulty=difficulty,
            board_size=self.board_size,
            on_game_end_callback=self.show_main_menu,
            two_player_mode=two_player_mode
        )
        game.play()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
