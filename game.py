import tkinter as tk
from tkinter import messagebox
from ai import TicTacToeAI
import subprocess
import sys
import json
import winsound
import random
import tkinter.font as tkFont
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "skip_turn_on_timeout": True,
            "sound_effects": True,
            "background_music": True,
            "volume": 70,
            "dark_mode": False,
            "board_animation": True,
            "language": "English",
            "leaderboard_enabled": True,
            "window_width": 600,
            "window_height": 600
        }

def restart_index():
    subprocess.Popen([sys.executable, r"index.py"])

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

def load_pixel_font(size=10):
    return tkFont.Font(family="Press Start 2P", size=size)

def animate_button_click(button):
    original_bg = button.cget("bg")
    button.configure(bg="white")
    button.after(100, lambda: button.configure(bg=original_bg))

class TicTacToe:
    def __init__(self, root, mode, difficulty, player1_name, player2_name, player_symbol):
        self.root = root
        self.root.title("Tic-Tac-Toe Game")
        self.settings = load_settings()

        width = self.settings.get("window_width", 600)
        height = self.settings.get("window_height", 600)
        center_window(root, width, height)
        root.configure(bg="#1e1e1e")
        self.pixel_font = load_pixel_font()

        self.mode = mode
        self.difficulty = difficulty
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player_symbol = player_symbol
        self.ai_symbol = "O" if player_symbol == "X" else "X"
        self.single_player = (mode == "single")
        self.ai = TicTacToeAI(ai_player=self.ai_symbol, difficulty=difficulty) if self.single_player else None
        self.current_player = random.choice(["X", "O"])

        self.board = [""] * 9
        self.buttons = []

        self.time_limit = 5
        self.remaining_time = self.time_limit
        self.timer_label = None
        self.timer_id = None

        if self.settings["background_music"]:
            self.play_background_music()

        self.create_menu()
        self.create_board()
        self.create_timer()

        if self.settings["dark_mode"]:
            self.apply_dark_mode()

        self.root.bind("<Configure>", self.resize_grid)

        starter_name = self.player1_name if self.current_player == self.player_symbol else self.player2_name
        messagebox.showinfo("Game Start", f"🎲 {starter_name} ({self.current_player}) starts!")

        if self.single_player and self.current_player == self.ai_symbol:
            self.ai_move()

    def create_board(self):
        for i in range(9):
            button = tk.Button(
                self.root,
                text="",
                font=self.pixel_font,
                width=5,
                height=2,
                bg="#1e1e1e",
                fg="#00f0ff",
                activebackground="#00f0ff",
                activeforeground="#1e1e1e",
                command=lambda i=i: self.make_move(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")
            self.buttons.append(button)

        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def create_timer(self):
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.remaining_time} s", font=self.pixel_font, fg="#00f0ff", bg="#1e1e1e")
        self.timer_label.grid(row=4, column=0, columnspan=3)
        self.start_timer()

    def start_timer(self):
        self.remaining_time = self.time_limit
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.remaining_time} s")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.skip_turn()

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def make_move(self, index):
        if self.buttons[index]["text"] == "" and not self.check_winner():
            self.stop_timer()

            if self.settings["sound_effects"]:
                self.play_click_sound()

            animate_button_click(self.buttons[index])
            self.buttons[index]["text"] = self.current_player
            self.board[index] = self.current_player
            winning_line = self.check_winner()

            if winning_line:
                if self.settings["board_animation"]:
                    self.animate_winning_line(winning_line)
                else:
                    self.show_winner_message()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "🤝 It's a draw!")
                self.ask_play_again()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.start_timer()
                if self.single_player and self.current_player == self.ai_symbol:
                    self.ai_move()

    def skip_turn(self):
        if self.settings["skip_turn_on_timeout"]:
            messagebox.showinfo("Turn Skipped", f"⏰ Time's up! {self.current_player}'s turn is skipped.")
            self.current_player = "O" if self.current_player == "X" else "X"
        self.start_timer()
        if self.single_player and self.current_player == self.ai_symbol:
            self.ai_move()

    def ai_move(self):
        move = self.ai.get_move(self.board)
        if move is not None:
            self.make_move(move)

    def check_winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in wins:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != "":
                return line
        return None

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button["text"] = ""
        self.current_player = random.choice(["X", "O"])
        starter_name = self.player1_name if self.current_player == self.player_symbol else self.player2_name
        messagebox.showinfo("Game Restarted", f"🎲 {starter_name} ({self.current_player}) starts!")
        self.start_timer()
        if self.single_player and self.current_player == self.ai_symbol:
            self.ai_move()

    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg="#1e1e1e")
        menu_frame.grid(row=3, column=0, columnspan=3, pady=10)

        quit_button = tk.Button(menu_frame, text="Quit", font=self.pixel_font, bg="#00f0ff", fg="#1e1e1e")
        quit_button.config(command=lambda: [animate_button_click(quit_button), self.confirm_quit()])
        quit_button.pack(side=tk.LEFT, padx=10)

        return_button = tk.Button(menu_frame, text="Return to Index", font=self.pixel_font, bg="#00f0ff", fg="#1e1e1e")
        return_button.config(command=lambda: [animate_button_click(return_button), self.return_to_index()])
        return_button.pack(side=tk.LEFT, padx=10)

    def return_to_index(self):
        self.root.destroy()
        restart_index()

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again", "Do you want to play again?")
        if answer:
            self.reset_game()
        else:
            self.root.quit()

    def confirm_quit(self):
        answer = messagebox.askyesno("Quit", "Are you sure you want to quit the game?")
        if answer:
            self.root.quit()

    def play_click_sound(self):
        try:
            winsound.Beep(600, 100)
        except:
            pass

    def play_background_music(self):
        try:
            winsound.PlaySound("8bit_theme.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            pass

    def apply_dark_mode(self):
        self.root.configure(bg="#1e1e1e")
        for button in self.buttons:
            button.configure(bg="#1e1e1e", fg="#00f0ff", activebackground="#00f0ff", activeforeground="#1e1e1e")
        self.timer_label.configure(bg="#1e1e1e", fg="#00f0ff")

    def animate_winning_line(self, line):
        def flash(count):
            color = "yellow" if count % 2 == 0 else "white"
            for idx in line:
                self.buttons[idx].configure(bg=color)
            if count < 5:
                self.root.after(300, flash, count + 1)
            else:
                self.show_winner_message()
        flash(0)

    def show_winner_message(self):
        winner_name = self.player1_name if self.current_player == self.player_symbol else self.player2_name
        messagebox.showinfo("Game Over", f"🎉 {winner_name} wins!")
        self.ask_play_again()

    def resize_grid(self, event):
        if event.width < 300 or event.height < 300:
            return

        cell_width = event.width // 3
        cell_height = (event.height - 150) // 3
        cell_size = min(cell_width, cell_height)
        font_size = max(10, min(cell_size // 3, 40))
        resized_font = tkFont.Font(family="Press Start 2P", size=font_size)

        for button in self.buttons:
            button.config(width=cell_size // 10, height=cell_size // 30, font=resized_font)

def start_game(mode, difficulty, player1_name, player2_name, player_symbol):
    root = tk.Tk()
    game = TicTacToe(root, mode, difficulty, player1_name, player2_name, player_symbol)
    root.mainloop()
