import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import sys
import json
import shutil
import os
from theme_utils import center_window, load_pixel_font, styled_button, get_current_theme

SETTINGS_FILE = "settings.json"
SAVE_FILE = "tictactoe_save.json"

def return_to_index():
    subprocess.Popen([sys.executable, r"index.py"])

class OptionsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Options")
        center_window(root, 600, 600)
        self.theme = get_current_theme()
        root.configure(bg=self.theme["background"])
        self.pixel_font = load_pixel_font()
        self.settings = self.load_settings()

        # Scrollable frame setup
        self.canvas = tk.Canvas(root, bg=self.theme["background"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.theme["background"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.create_options_content()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_options_content(self):
        # Theme Selector
        tk.Label(self.scrollable_frame, text="Choose Theme", font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"]).pack(pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "pixel_night"))
        tk.OptionMenu(self.scrollable_frame, self.theme_var, *["pixel_night", "retro_arcade", "classic_light"]).pack()

        # Skip Turn
        self.skip_turn = tk.BooleanVar(value=self.settings["skip_turn_on_timeout"])
        tk.Checkbutton(self.scrollable_frame, text="Skip Turn on Timeout", variable=self.skip_turn, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Sound Effects
        self.sound_effects = tk.BooleanVar(value=self.settings["sound_effects"])
        tk.Checkbutton(self.scrollable_frame, text="Enable Sound Effects", variable=self.sound_effects, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Background Music
        self.background_music = tk.BooleanVar(value=self.settings["background_music"])
        tk.Checkbutton(self.scrollable_frame, text="Enable Background Music", variable=self.background_music, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Volume
        tk.Label(self.scrollable_frame, text="Volume (0-100%)", font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"]).pack(pady=5)
        self.volume = tk.Scale(self.scrollable_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg="#333", fg=self.theme["font_color"], troughcolor="#555")
        self.volume.set(self.settings["volume"])
        self.volume.pack()

        # Dark Mode
        self.dark_mode = tk.BooleanVar(value=self.settings["dark_mode"])
        tk.Checkbutton(self.scrollable_frame, text="Enable Dark Mode", variable=self.dark_mode, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Board Animation
        self.board_animation = tk.BooleanVar(value=self.settings["board_animation"])
        tk.Checkbutton(self.scrollable_frame, text="Enable Board Animation", variable=self.board_animation, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Language
        tk.Label(self.scrollable_frame, text="Select Language", font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"]).pack(pady=5)
        self.language = tk.StringVar(value=self.settings["language"])
        tk.OptionMenu(self.scrollable_frame, self.language, "English", "French").pack()

        # Leaderboard
        self.leaderboard = tk.BooleanVar(value=self.settings["leaderboard_enabled"])
        tk.Checkbutton(self.scrollable_frame, text="Enable Leaderboard Tracking", variable=self.leaderboard, font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"], selectcolor="#333").pack(anchor=tk.W, pady=5)

        # Window Size
        tk.Label(self.scrollable_frame, text="Window Width", font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"]).pack(pady=5)
        self.window_width = tk.Scale(self.scrollable_frame, from_=400, to=800, orient=tk.HORIZONTAL, bg="#333", fg=self.theme["font_color"], troughcolor="#555")
        self.window_width.set(self.settings.get("window_width", 600))
        self.window_width.pack()

        tk.Label(self.scrollable_frame, text="Window Height", font=self.pixel_font, bg=self.theme["background"], fg=self.theme["font_color"]).pack(pady=5)
        self.window_height = tk.Scale(self.scrollable_frame, from_=400, to=800, orient=tk.HORIZONTAL, bg="#333", fg=self.theme["font_color"], troughcolor="#555")
        self.window_height.set(self.settings.get("window_height", 600))
        self.window_height.pack()

        # Action Buttons
        action_frame = tk.Frame(self.scrollable_frame, bg=self.theme["background"])
        action_frame.pack(pady=20)

        styled_button(action_frame, "Save Settings", self.save_settings).pack(side=tk.LEFT, padx=10)
        styled_button(action_frame, "Backup Settings", self.backup_settings).pack(side=tk.LEFT, padx=10)
        styled_button(action_frame, "Restore Settings", self.restore_settings).pack(side=tk.LEFT, padx=10)

        styled_button(self.scrollable_frame, "Clear Saved Game & Reset Settings", self.clear_all).pack(pady=10)
        styled_button(self.scrollable_frame, "Back to Main Menu", self.go_back).pack(pady=10)

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "theme": "pixel_night",
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

    def save_settings(self):
        data = {
            "theme": self.theme_var.get(),
            "skip_turn_on_timeout": self.skip_turn.get(),
            "sound_effects": self.sound_effects.get(),
            "background_music": self.background_music.get(),
            "volume": self.volume.get(),
            "dark_mode": self.dark_mode.get(),
            "board_animation": self.board_animation.get(),
            "language": self.language.get(),
            "leaderboard_enabled": self.leaderboard.get(),
            "window_width": self.window_width.get(),
            "window_height": self.window_height.get()
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Saved", "✅ Settings saved successfully!")

    def backup_settings(self):
        backup_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if backup_path:
            shutil.copy(SETTINGS_FILE, backup_path)
            messagebox.showinfo("Backup", "🟢 Settings backed up successfully!")

    def restore_settings(self):
        restore_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if restore_path:
            shutil.copy(restore_path, SETTINGS_FILE)
            messagebox.showinfo("Restored", "🟢 Settings restored successfully!")
            self.root.destroy()
            subprocess.Popen([sys.executable, __file__])

    def clear_all(self):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        messagebox.showinfo("Cleared", "🧹 Saved game and settings have been cleared!")
        self.root.destroy()
        subprocess.Popen([sys.executable, __file__])

    def go_back(self):
        self.root.destroy()
        return_to_index()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptionsWindow(root)
    root.mainloop()
