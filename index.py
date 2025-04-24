import tkinter as tk
import subprocess
import sys
from theme_utils import center_window, load_pixel_font, styled_button

def open_setup_window():
    subprocess.Popen([sys.executable, r"C:\Users\DELL\Documents\own_work\game\tic_tac_toe\setup_window.py"])

def open_options_window():
    subprocess.Popen([sys.executable, r"C:\Users\DELL\Documents\own_work\game\tic_tac_toe\options_window.py"])

def main():
    root = tk.Tk()
    root.title("Tic-Tac-Toe Main Menu")
    center_window(root, 600, 600)
    root.configure(bg="#1e1e1e")
    pixel_font = load_pixel_font()

    tk.Label(root, text="Tic-Tac-Toe", font=pixel_font, bg="#1e1e1e", fg="#00f0ff").pack(pady=20)
    styled_button(root, "Play", open_setup_window).pack(pady=10)
    styled_button(root, "Options", open_options_window).pack(pady=10)
    styled_button(root, "Quit", root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
