import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk

# -------------------- APP CONFIG --------------------

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

# -------------------- WORD BANK --------------------

WORDS = {
    "Easy": ["cat", "dog", "sun", "tree"],
    "Medium": ["border", "promise", "plants"],
    "Hard": ["programming", "cybersecurity", "algorithm"]
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
        self.geometry("620x720")
        self.resizable(False, False)

        self.difficulty = ctk.StringVar(value="Medium")
        self.theme = "dark"

        pygame.mixer.init()
        self.load_sounds()
        self.load_images()
        self.create_widgets()
        self.start_game()

    # -------------------- LOAD ASSETS --------------------

    def load_images(self):
        self.images = []
        for i in range(7):
            img = Image.open(f"assets/Hangman-{i}.gif").resize((320, 260))
            self.images.append(ImageTk.PhotoImage(img))

    def load_sounds(self):
        self.sound_correct = pygame.mixer.Sound("sounds/correct.wav")
        self.sound_wrong = pygame.mixer.Sound("sounds/wrong.wav")
        self.sound_win = pygame.mixer.Sound("sounds/win.wav")
        self.sound_lose = pygame.mixer.Sound("sounds/lose.wav")
        self.sound_click = pygame.mixer.Sound("sounds/click.wav")

    def play_click(self):
        self.sound_click.play()

    # -------------------- GAME SETUP --------------------

    def start_game(self):
        level = self.difficulty.get()
        self.word = random.choice(WORDS[level])
        self.display = ["_"] * len(self.word)
        self.attempts = ATTEMPTS[level]
        self.stage = 0
        self.guessed = []
        self.hint_used = False

        self.update_ui()
        self.image_label.configure(image=self.images[0])
        self.entry.configure(state="normal")

    # -------------------- UI --------------------

    def create_widgets(self):

        ctk.CTkLabel(
            self,
            text="HANGMAN",
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Toggle Light / Dark",
            command=self.toggle_theme
        ).pack(pady=5)

        diff_frame = ctk.CTkFrame(self)
        diff_frame.pack(pady=10)

        for level in ["Easy", "Medium", "Hard"]:
            ctk.CTkRadioButton(
                diff_frame,
                text=level,
                variable=self.difficulty,
                value=level,
                command=self.start_game
            ).pack(side="left", padx=15)

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(pady=15)

        self.word_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=22))
        self.word_label.pack(pady=10)

        self.attempts_label = ctk.CTkLabel(self)
        self.attempts_label.pack()

        self.guessed_label = ctk.CTkLabel(self)
        self.guessed_label.pack(pady=5)

        self.entry = ctk.CTkEntry(self, width=80, justify="center")
        self.entry.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Guess",
            command=lambda: [self.play_click(), self.check_guess()]
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Hint (1 only)",
            fg_color="orange",
            command=lambda: [self.play_click(), self.use_hint()]
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Restart Game",
            fg_color="gray",
            command=lambda: [self.play_click(), self.start_game()]
        ).pack(pady=10)

    # -------------------- GAME LOGIC --------------------

    def check_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, ctk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Enter one alphabet only")
            return

        if guess in self.guessed:
            return

        self.guessed.append(guess)

        if guess in self.word:
            self.sound_correct.play()
            for i, ch in enumerate(self.word):
                if ch == guess:
                    self.display[i] = guess
        else:
            self.sound_wrong.play()
            self.fail_attempt()

        self.update_ui()
        self.check_game_over()

    def use_hint(self):
        if self.hint_used:
            messagebox.showinfo("Hint", "Hint already used")
            return

        hidden = [i for i, c in enumerate(self.display) if c == "_"]
        if not hidden:
            return

        index = random.choice(hidden)
        self.display[index] = self.word[index]
        self.hint_used = True
        self.sound_wrong.play()
        self.fail_attempt()

        self.update_ui()
        self.check_game_over()

    def fail_attempt(self):
        self.attempts -= 1
        self.stage += 1
        self.image_label.configure(image=self.images[self.stage])

    # -------------------- UI UPDATE --------------------

    def update_ui(self):
        self.word_label.configure(text=" ".join(self.display))
        self.attempts_label.configure(text=f"Attempts left: {self.attempts}")
        self.guessed_label.configure(text="Guessed: " + ", ".join(self.guessed))

    def check_game_over(self):
        if "_" not in self.display:
            self.sound_win.play()
            messagebox.showinfo("Victory", "🎉 You Won!")
            self.entry.configure(state="disabled")

        elif self.attempts == 0:
            self.sound_lose.play()
            messagebox.showerror("Game Over", f"Word was: {self.word}")
            self.entry.configure(state="disabled")

    # -------------------- THEME --------------------

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        ctk.set_appearance_mode(self.theme)

# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()
