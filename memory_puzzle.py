import tkinter as tk
import random
from tkinter import messagebox

EMOJI_PAIRS = [
    ('🍓', 'fruit', 'red'),
    ('🍎', 'fruit', 'red'),
    ('🐶', 'animal', 'green'),
    ('🐒', 'animal', 'green'),
    ('🦁', 'animal', 'green'),
    ('🐢', 'reptile', 'orange'),
    ('🐍', 'reptile', 'orange'),
    ('🦎', 'reptile', 'orange'),
]

CARD_BACK = "❓"
TIMER_SECONDS = 60


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Memory Puzzle Game")
        self.root.geometry("800x750") 
        self.root.configure(bg="#f5f5dc")

        # Game variables
        self.buttons = []
        self.card_values = []
        self.card_colors = []
        self.first = None
        self.second = None
        self.matches_found = 0
        self.remaining_time = TIMER_SECONDS
      
        self.info_label = tk.Label(root, text="🎮 Click 'Start Game' to begin!", font=("Arial", 16, "bold"),
                                   bg="#f5f5dc", fg="black")
        self.info_label.grid(row=0, column=0, columnspan=4, pady=(10, 10))

        for i in range(4):
            for j in range(4):
                btn = tk.Button(root, text="", font=("Arial", 30), width=4, height=2,
                                bg="#dcdcdc", fg="black",
                                command=lambda idx=4 * i + j: self.reveal_card(idx),
                                state="disabled")
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        # Timer label
        self.timer_label = tk.Label(root, text="", font=("Arial", 14), bg="#f5f5dc", fg="black")
        self.timer_label.grid(row=5, column=0, columnspan=4, pady=(10, 5))

        # Start/End Buttons
        self.start_button = tk.Button(root, text="▶️ Start Game", command=self.start_game,
                                      bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=15)

        self.end_button = tk.Button(root, text="⏹ End Game", command=self.end_game,
                                    bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=15, state="disabled")
        self.end_button.grid(row=6, column=2, columnspan=2, pady=15)

    def start_game(self):
        self.info_label.config(text="🧠 Match all the emoji pairs!")
        self.matches_found = 0
        self.remaining_time = TIMER_SECONDS
        self.first = None
        self.second = None

        # Shuffle emojis
        emoji_set = EMOJI_PAIRS.copy()
        emojis = emoji_set * 2
        random.shuffle(emojis)

        self.card_values = [e[0] for e in emojis]
        self.card_colors = [e[2] for e in emojis]

        for btn in self.buttons:
            btn.config(text=CARD_BACK, state="normal", bg="#dcdcdc", fg="black")

        self.start_button.config(state="disabled")
        self.end_button.config(state="normal")
        self.update_timer()

    def reveal_card(self, index):
        if self.buttons[index]["text"] != CARD_BACK or self.second is not None:
            return

        emoji = self.card_values[index]
        color = self.card_colors[index]
        self.buttons[index].config(text=emoji, fg=color)

        if self.first is None:
            self.first = index
        else:
            self.second = index
            self.root.after(700, self.check_match)

    def check_match(self):
        i1, i2 = self.first, self.second
        if self.card_values[i1] == self.card_values[i2]:
            self.info_label.config(text="✅ Matched!")
            self.matches_found += 1
            if self.matches_found == len(EMOJI_PAIRS):
                self.end_game(won=True)
        else:
            self.info_label.config(text="❌ Unmatched!")
            self.buttons[i1].config(text=CARD_BACK, fg="black")
            self.buttons[i2].config(text=CARD_BACK, fg="black")

        self.first = None
        self.second = None

    def update_timer(self):
        self.timer_label.config(text=f"⏱ Time Left: {self.remaining_time}s")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.matches_found < len(EMOJI_PAIRS):
            self.end_game(won=False)

    def end_game(self, won=None):
        for btn in self.buttons:
            btn.config(state="disabled")
        self.start_button.config(state="normal")
        self.end_button.config(state="disabled")

        if won is None:
            self.info_label.config(text="🛑 Game Ended by User.")
        elif won:
            self.info_label.config(text="🎉 You matched all pairs! You Win!")
            messagebox.showinfo("Victory", "🎉 Congratulations! You matched all pairs!")
        else:
            self.info_label.config(text="⏰ Time's up! Try Again!")
            messagebox.showinfo("Game Over", "⏰ Time's up! Try again!")

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
