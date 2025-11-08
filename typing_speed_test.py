import tkinter as tk
import random
WORDS = [
    "galaxy", "neon", "python", "hackerz", "moonshot", "matrix", "logic",
    "quantum", "cyber", "fusion", "pixel", "glitch", "vortex", "cloud",
    "system", "debug", "binary", "compile", "execute", "infinity"
]

class UltraTypingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test! ")
        self.root.geometry("900x600")
        self.root.config(bg="#0d1117")

        # Theme colors
        self.bg_color = "#0d1117"
        self.neon_blue = "#00e0ff"
        self.neon_purple = "#9b4dff"
        self.text_color = "#ffffff"

        self.time_limit = 30
        self.time_left = self.time_limit
        self.timer_running = False
        self.score = 0
        self.word = ""

        self.build_ui()

    def build_ui(self):
        self.title_label = tk.Label(
            self.root,
            text=" Typing Speed Test ",
            font=("Segoe UI", 28, "bold"),
            fg=self.neon_blue,
            bg=self.bg_color
        )
        self.title_label.pack(pady=20)

        self.glow_colors = [self.neon_blue, self.neon_purple]
        self.glow_index = 0
        self.animate_glow()

        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(pady=30)

        self.timer_canvas = tk.Canvas(
            frame, width=180, height=180, bg=self.bg_color, highlightthickness=0
        )
        self.timer_canvas.grid(row=0, column=0, padx=50)
        self.arc = self.timer_canvas.create_oval(20, 20, 160, 160, outline=self.neon_purple, width=6)
        self.timer_text = self.timer_canvas.create_text(
            90, 90, text=f"{self.time_left}", fill=self.text_color, font=("Consolas", 24, "bold")
        )

        self.word_label = tk.Label(
            frame, text="Press Start", font=("Consolas", 26, "bold"),
            fg=self.neon_blue, bg=self.bg_color
        )
        self.word_label.grid(row=0, column=1, padx=50)

        self.entry = tk.Entry(
            self.root, font=("Consolas", 20),
            bg="#161b22", fg=self.text_color, insertbackground=self.neon_blue,
            width=25, justify="center", relief="flat"
        )
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", self.check_word)

        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)

        self.start_btn = tk.Button(
            button_frame, text=" START",
            command=self.start_game,
            font=("Segoe UI", 14, "bold"),
            bg=self.neon_blue, fg="#000", activebackground=self.neon_purple,
            width=10, relief="flat", cursor="hand2"
        )
        self.start_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = tk.Button(
            button_frame, text=" RESET",
            command=self.reset_game,
            font=("Segoe UI", 14, "bold"),
            bg=self.neon_purple, fg="#fff", activebackground=self.neon_blue,
            width=10, relief="flat", cursor="hand2"
        )
        self.reset_btn.grid(row=0, column=1, padx=10)

        self.score_label = tk.Label(
            self.root, text="Score: 0", font=("Consolas", 18, "bold"),
            fg=self.text_color, bg=self.bg_color
        )
        self.score_label.pack(pady=10)

        footer = tk.Label(
            self.root,
            text=" Typing Arena ",
            font=("Consolas", 12, "italic"),
            fg="#888", bg=self.bg_color
        )
        footer.pack(side="bottom", pady=10)

    def animate_glow(self):
        self.glow_index = (self.glow_index + 1) % len(self.glow_colors)
        self.title_label.config(fg=self.glow_colors[self.glow_index])
        self.root.after(500, self.animate_glow)

    def start_game(self):
        if not self.timer_running:
            self.timer_running = True
            self.time_left = self.time_limit
            self.score = 0
            self.update_word()
            self.update_timer()
            self.entry.delete(0, tk.END)
            self.entry.focus()

    def update_word(self):
        self.word = random.choice(WORDS)
        self.word_label.config(text=self.word)

    def check_word(self, event=None):
        if not self.timer_running:
            return
        typed = self.entry.get().strip()
        if typed.lower() == self.word.lower():
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.update_word()
        self.entry.delete(0, tk.END)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_canvas.itemconfig(self.timer_text, text=f"{self.time_left}")
            self.draw_timer_arc()
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def draw_timer_arc(self):
        angle = 360 * (self.time_left / self.time_limit)
        self.timer_canvas.delete("progress")
        self.timer_canvas.create_arc(
            20, 20, 160, 160, start=90, extent=-angle,
            style="arc", outline=self.neon_blue, width=6, tags="progress"
        )

    def end_game(self):
        self.timer_running = False
        wpm = round((self.score / self.time_limit) * 60, 2)
        self.word_label.config(
            text=f" Time is Up!\nFinal Score: {self.score}\nAvg Speed: {wpm} WPM "
        )
        self.entry.delete(0, tk.END)

    def reset_game(self):
        self.timer_running = False
        self.time_left = self.time_limit
        self.score = 0
        self.word_label.config(text="Press Start")
        self.score_label.config(text="Score: 0")
        self.timer_canvas.itemconfig(self.timer_text, text=f"{self.time_left}")
        self.timer_canvas.delete("progress")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraTypingUI(root)
    root.mainloop()
