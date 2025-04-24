import tkinter as tk
import tkinter.font as tkFont
import json

SETTINGS_FILE = "settings.json"

# Available themes
THEMES = {
    "pixel_night": {
        "background": "#1e1e1e",
        "button_bg": "#00f0ff",
        "button_fg": "#1e1e1e",
        "font_family": "Press Start 2P",
        "font_color": "#00f0ff"
    },
    "retro_arcade": {
        "background": "#000000",
        "button_bg": "#ff00ff",
        "button_fg": "#ffffff",
        "font_family": "Press Start 2P",
        "font_color": "#ff00ff"
    },
    "classic_light": {
        "background": "#ffffff",
        "button_bg": "#cccccc",
        "button_fg": "#000000",
        "font_family": "Arial",
        "font_color": "#333333"
    }
}

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"theme": "pixel_night"}

def get_current_theme():
    settings = load_settings()
    theme_name = settings.get("theme", "pixel_night")
    return THEMES.get(theme_name, THEMES["pixel_night"])

def load_pixel_font(size=10):
    try:
        return tkFont.Font(family="Press Start 2P", size=size)
    except:
        return tkFont.Font(size=size)

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

def animate_button_click(button):
    original_bg = button.cget("bg")
    button.configure(bg="white")
    button.after(100, lambda: button.configure(bg=original_bg))

def styled_button(root, text, command):
    theme = get_current_theme()
    font = load_pixel_font() if theme["font_family"] == "Press Start 2P" else tkFont.Font(family=theme["font_family"], size=10)
    button = tk.Button(
        root,
        text=text,
        font=font,
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_bg"],
        activeforeground=theme["button_fg"],
        command=lambda: [animate_button_click(button), command()]
    )
    return button
