import tkinter as tk
from game import start_game
from theme_utils import center_window, load_pixel_font, styled_button

class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Setup")
        center_window(root, 600, 600)
        root.configure(bg="#1e1e1e")
        pixel_font = load_pixel_font()

        self.mode = tk.StringVar(value="single")
        self.difficulty = tk.StringVar(value="easy")
        self.player_symbol = tk.StringVar(value="X")

        tk.Label(root, text="Choose Game Mode", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=10)
        tk.Radiobutton(root, text="Player vs AI", variable=self.mode, value="single", font=pixel_font, bg="#1e1e1e", fg="#00f0ff", selectcolor="#333").pack(anchor=tk.W)
        tk.Radiobutton(root, text="Player vs Player", variable=self.mode, value="two", font=pixel_font, bg="#1e1e1e", fg="#00f0ff", selectcolor="#333").pack(anchor=tk.W)

        tk.Label(root, text="Choose AI Difficulty", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=10)
        for text, value in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            tk.Radiobutton(root, text=text, variable=self.difficulty, value=value, font=pixel_font, bg="#1e1e1e", fg="#00f0ff", selectcolor="#333").pack(anchor=tk.W)

        tk.Label(root, text="Player X Name:", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=5)
        self.player1_entry = tk.Entry(root, font=pixel_font, bg="#333", fg="#00f0ff")
        self.player1_entry.pack()

        tk.Label(root, text="Player O Name / AI Name:", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=5)
        self.player2_entry = tk.Entry(root, font=pixel_font, bg="#333", fg="#00f0ff")
        self.player2_entry.pack()

        tk.Label(root, text="Choose Your Symbol", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=10)
        tk.Radiobutton(root, text="X", variable=self.player_symbol, value="X", font=pixel_font, bg="#1e1e1e", fg="#00f0ff", selectcolor="#333").pack(anchor=tk.W)
        tk.Radiobutton(root, text="O", variable=self.player_symbol, value="O", font=pixel_font, bg="#1e1e1e", fg="#00f0ff", selectcolor="#333").pack(anchor=tk.W)

        styled_button(root, "Start Game", self.launch_game).pack(pady=20)

    def launch_game(self):
        mode = self.mode.get()
        difficulty = self.difficulty.get()
        player1_name = self.player1_entry.get() or "Player X"
        player2_name = self.player2_entry.get() or ("AI" if mode == "single" else "Player O")
        symbol = self.player_symbol.get()

        self.root.destroy()
        start_game(mode, difficulty, player1_name, player2_name, symbol)

if __name__ == "__main__":
    root = tk.Tk()
    app = SetupWindow(root)
    root.mainloop()
# This code is part of a Tic-Tac-Toe game setup window that allows users to select game mode, difficulty, player names, and symbols.