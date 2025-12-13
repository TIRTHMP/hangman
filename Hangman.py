import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random

# -------------------- APP SETTINGS --------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------- WORD BANK --------------------

WORD_BANK = {
    "Easy": ["cat", "dog", "sun", "book", "tree"],
    "Medium": ["border", "promise", "rhyme", "plants"],
    "Hard": ["programming", "cybersecurity", "algorithm", "artificial"]
}

ATTEMPTS = {
    "Easy": 7,
    "Medium": 5,
    "Hard": 4
}

# -------------------- MAIN APP --------------------

class HangmanApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("600x650")
        self.resizable(False, False)

        self.difficulty = ctk.StringVar(value="Medium")

        self.create_widgets()
        self.start_game()

    # -------------------- GAME SETUP --------------------

    def start_game(self):
        level = self.difficulty.get()
        self.word = random.choice(WORD_BANK[level])
        self.display = ["_"] * len(self.word)
        self.attempts = ATTEMPTS[level]
        self.guessed = []
        self.stage = 0

        self.update_ui()
        self.canvas.delete("all")
        self.draw_gallows()
        self.entry.configure(state="normal")

    # -------------------- UI --------------------

    def create_widgets(self):

        ctk.CTkLabel(
            self,
            text="HANGMAN",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=15)

        # Difficulty selector
        diff_frame = ctk.CTkFrame(self)
        diff_frame.pack(pady=5)

        for level in ["Easy", "Medium", "Hard"]:
            ctk.CTkRadioButton(
                diff_frame,
                text=level,
                variable=self.difficulty,
                value=level,
                command=self.start_game
            ).pack(side="left", padx=15)

        # Canvas
        self.canvas = tk.Canvas(self, width=320, height=260, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=15)

        self.word_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(size=22)
        )
        self.word_label.pack(pady=10)

        self.attempts_label = ctk.CTkLabel(self)
        self.attempts_label.pack()

        self.guessed_label = ctk.CTkLabel(self)
        self.guessed_label.pack(pady=5)

        self.entry = ctk.CTkEntry(
            self,
            width=80,
            justify="center",
            font=ctk.CTkFont(size=16)
        )
        self.entry.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Guess",
            command=self.check_guess,
            width=120
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Restart Game",
            command=self.start_game,
            fg_color="gray"
        ).pack(pady=5)

    # -------------------- GAME LOGIC --------------------

    def check_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, ctk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Enter one alphabet only")
            return

        if guess in self.guessed:
            messagebox.showinfo("Info", "Letter already guessed")
            return

        self.guessed.append(guess)

        if guess in self.word:
            for i, ch in enumerate(self.word):
                if ch == guess:
                    self.display[i] = guess
        else:
            self.attempts -= 1
            self.stage += 1
            self.draw_hangman()

        self.update_ui()

        if "_" not in self.display:
            messagebox.showinfo("Victory", "🎉 You won!")
            self.entry.configure(state="disabled")

        elif self.attempts == 0:
            messagebox.showerror("Game Over", f"Word was: {self.word}")
            self.entry.configure(state="disabled")

    # -------------------- UI UPDATE --------------------

    def update_ui(self):
        self.word_label.configure(text=" ".join(self.display))
        self.attempts_label.configure(text=f"Attempts left: {self.attempts}")
        self.guessed_label.configure(text="Guessed: " + ", ".join(self.guessed))

    # -------------------- DRAWING --------------------

    def draw_gallows(self):
        c = self.canvas
        c.create_line(60, 240, 260, 240, fill="white", width=3)
        c.create_line(110, 240, 110, 40, fill="white", width=3)
        c.create_line(110, 40, 200, 40, fill="white", width=3)
        c.create_line(200, 40, 200, 70, fill="white", width=3)

    def draw_hangman(self):
        c = self.canvas
        s = self.stage

        if s == 1:
            c.create_oval(180, 70, 220, 110, outline="white", width=2)
        elif s == 2:
            c.create_line(200, 110, 200, 160, fill="white", width=2)
        elif s == 3:
            c.create_line(200, 120, 170, 140, fill="white", width=2)
        elif s == 4:
            c.create_line(200, 120, 230, 140, fill="white", width=2)
        elif s == 5:
            c.create_line(200, 160, 170, 200, fill="white", width=2)
        elif s == 6:
            c.create_line(200, 160, 230, 200, fill="white", width=2)

# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()
