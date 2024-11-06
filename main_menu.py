import tkinter as tk
from go_game import GoGame


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Go Game")
        self.root.geometry("500x700")
        self.root.configure(bg="#F4A460")

        self.main_frame = tk.Frame(self.root, bg="#F4A460")
        self.main_frame.pack(fill="both", expand=True)

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
            font=("Arial", 24, "bold"),
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

        exit_button = tk.Button(self.main_frame, text="Выход", command=self.root.quit)
        self.style_button(exit_button)
        exit_button.pack(pady=10)

    def show_difficulty_selection(self):
        self.clear_frame()

        label = tk.Label(
            self.main_frame,
            text="Выберите уровень сложности:",
            font=("Arial", 16, "bold"),
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
            font=("Arial", 18, "bold"),
            fg="#8B4513",
            bg="#F4A460"
        )
        label.pack(pady=20)

        sample_text = "1. Игрок 1 - 100 очков\n2. Игрок 2 - 80 очков\n3. Игрок 3 - 70 очков"
        leaderboard_label = tk.Label(
            self.main_frame,
            text=sample_text,
            font=("Arial", 14),
            fg="#8B4513",
            bg="#F4A460"
        )
        leaderboard_label.pack(pady=20)

        back_button = tk.Button(self.main_frame, text="Назад", command=self.show_main_menu)
        self.style_button(back_button)
        back_button.pack(pady=10)

    def start_game(self, difficulty):
        self.clear_frame()

        game = GoGame(parent=self.main_frame, difficulty=difficulty, on_game_end_callback=self.show_main_menu)
        game.play()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
