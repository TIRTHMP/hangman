import tkinter as tk
from tkinter import messagebox
import random

# -------------------- GAME SETUP --------------------

WORDS = [
    "january", "border", "image", "film", "promise",
    "kids", "lungs", "doll", "rhyme", "damage", "plants"
]

MAX_ATTEMPTS = 5

# -------------------- MAIN CLASS --------------------

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        self.start_game()
        self.create_widgets()

    # -------------------- GAME LOGIC --------------------

    def start_game(self):
        self.word = random.choice(WORDS)
        self.display = ["_"] * len(self.word)
        self.attempts = MAX_ATTEMPTS
        self.guessed_letters = []

    # -------------------- GUI LAYOUT --------------------

    def create_widgets(self):
        self.title = tk.Label(
            self.root,
            text="HANGMAN GAME",
            font=("Arial", 22, "bold")
        )
        self.title.pack(pady=10)

        self.word_label = tk.Label(
            self.root,
            text=" ".join(self.display),
            font=("Arial", 18)
        )
        self.word_label.pack(pady=20)

        self.attempts_label = tk.Label(
            self.root,
            text=f"Attempts left: {self.attempts}",
            font=("Arial", 12)
        )
        self.attempts_label.pack(pady=5)

        self.guessed_label = tk.Label(
            self.root,
            text="Guessed letters: ",
            font=("Arial", 10)
        )
        self.guessed_label.pack(pady=5)

        self.entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=5,
            justify="center"
        )
        self.entry.pack(pady=10)
        self.entry.focus()

        self.guess_button = tk.Button(
            self.root,
            text="Guess",
            font=("Arial", 12),
            command=self.check_guess
        )
        self.guess_button.pack(pady=10)

        self.restart_button = tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 10),
            command=self.restart_game
        )
        self.restart_button.pack(pady=5)

    # -------------------- GAME FUNCTION --------------------

    def check_guess(self):
        guess = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter ONE alphabet letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Info", "You already guessed this letter.")
            return

        self.guessed_letters.append(guess)
        self.guessed_label.config(
            text="Guessed letters: " + ", ".join(self.guessed_letters)
        )

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.display[i] = guess
        else:
            self.attempts -= 1

        self.word_label.config(text=" ".join(self.display))
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

        if "_" not in self.display:
            messagebox.showinfo("Congratulations!", "You guessed the word correctly 🎉")
            self.disable_game()

        elif self.attempts == 0:
            messagebox.showerror(
                "Game Over",
                f"You are hanged!\nThe word was: {self.word}"
            )
            self.disable_game()

    # -------------------- HELPER FUNCTIONS --------------------

    def disable_game(self):
        self.guess_button.config(state="disabled")
        self.entry.config(state="disabled")

    def restart_game(self):
        self.start_game()
        self.word_label.config(text=" ".join(self.display))
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        self.guessed_label.config(text="Guessed letters: ")
        self.guess_button.config(state="normal")
        self.entry.config(state="normal")
        self.entry.focus()

# -------------------- RUN APP --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
