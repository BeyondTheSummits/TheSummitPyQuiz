# Python Quiz - Tkinter version
# Uses your existing question modules: easy.py, medium.py and hard.py.
# Keep this file in the SAME folder as those three files.

import tkinter as tk
from tkinter import ttk

from easy import easy_questions
from medium import medium_questions
from hard import hard_questions

START_LIVES = 3

LEVELS = {
    "Level 1: Easy": ("Easy", easy_questions),
    "Level 2: Medium": ("Medium", medium_questions),
    "Level 3: Hard": ("Hard", hard_questions),
}

GREEN = "#1b7a3d"
RED = "#b3261e"
LIGHT_GREEN = "#c8e6c9"
LIGHT_RED = "#f5c6c2"


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Quiz")
        self.geometry("680x560")
        self.minsize(600, 520)

        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Sub.TLabel", font=("Segoe UI", 11))
        style.configure("Big.TButton", font=("Segoe UI", 11), padding=8)

        self.container = ttk.Frame(self, padding=24)
        self.container.pack(fill="both", expand=True)

        # quiz state
        self.level_name = ""
        self.level_key = ""
        self.items = []
        self.index = 0
        self.score = 0
        self.lives = START_LIVES
        self.answered = False

        self.show_start()

    # ---------- helpers ----------
    def clear(self):
        self.unbind("<Return>")
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------- start screen ----------
    def show_start(self):
        self.clear()
        ttk.Label(self.container, text="Welcome to Python Quiz!", style="Title.TLabel").pack(pady=(30, 8))
        ttk.Label(self.container, text="This quiz is designed to test your coding knowledge.",
                  style="Sub.TLabel").pack()
        ttk.Label(self.container, text=f"You have {START_LIVES} lives. Good luck!",
                  style="Sub.TLabel").pack(pady=(4, 30))
        ttk.Label(self.container, text="Which difficulty would you like to play on?",
                  style="Sub.TLabel").pack(pady=(0, 10))

        for label, (_, questions) in LEVELS.items():
            ttk.Button(self.container, text=label, style="Big.TButton", width=24,
                       command=lambda l=label: self.start_quiz(l)).pack(pady=5)

        ttk.Button(self.container, text="Quit", command=self.destroy).pack(pady=(25, 0))

    # ---------- starting / resetting a quiz ----------
    def start_quiz(self, level_key):
        self.level_key = level_key
        self.level_name, questions = LEVELS[level_key]
        self.items = list(questions.items())
        self.index = 0
        self.score = 0
        self.lives = START_LIVES
        self.show_question()

    # ---------- question screen ----------
    def show_question(self):
        self.clear()
        self.answered = False
        question, data = self.items[self.index]

        # Header: level, question number, score, lives
        header = ttk.Frame(self.container)
        header.pack(fill="x")
        ttk.Label(header, text=f"{self.level_name}  •  Question {self.index + 1} of {len(self.items)}",
                  style="Sub.TLabel").pack(side="left")
        self.stats_var = tk.StringVar()
        ttk.Label(header, textvariable=self.stats_var, style="Sub.TLabel").pack(side="right")
        self.refresh_stats()

        bar = ttk.Progressbar(self.container, maximum=len(self.items), value=self.index)
        bar.pack(fill="x", pady=(8, 16))

        # Question text (can contain line breaks for code)
        tk.Label(self.container, text=question, font=("Consolas", 13), justify="left",
                 anchor="w", wraplength=600).pack(fill="x", pady=(0, 14))

        self.option_buttons = {}
        self.entry = None

        if "options" in data:
            # Multiple choice: one button per option
            for line in data["options"].split("\n"):
                letter = line.split(".")[0].strip().upper()
                btn = tk.Button(self.container, text=line, font=("Segoe UI", 11), anchor="w",
                                padx=12, pady=6, relief="groove",
                                command=lambda l=letter: self.submit(l))
                btn.pack(fill="x", pady=3)
                self.option_buttons[letter] = btn
        else:
            # Typed answer
            row = ttk.Frame(self.container)
            row.pack(fill="x", pady=4)
            self.answer_var = tk.StringVar()
            self.entry = ttk.Entry(row, textvariable=self.answer_var, font=("Segoe UI", 12))
            self.entry.pack(side="left", fill="x", expand=True)
            self.entry.focus()
            self.submit_btn = ttk.Button(row, text="Submit",
                                         command=lambda: self.submit(self.answer_var.get()))
            self.submit_btn.pack(side="left", padx=(8, 0))
            self.bind("<Return>", lambda e: self.on_enter(data))

        # Feedback and Next button
        self.feedback = tk.Label(self.container, text="", font=("Segoe UI", 12, "bold"),
                                 justify="left", anchor="w", wraplength=600)
        self.feedback.pack(fill="x", pady=(14, 4))

        self.next_btn = ttk.Button(self.container, text="Next question", state="disabled",
                                   command=self.next_step)
        self.next_btn.pack(anchor="e", pady=(4, 0))

    def on_enter(self, data):
        # Enter submits the typed answer, or moves on once answered
        if not self.answered:
            self.submit(self.answer_var.get())
        elif str(self.next_btn["state"]) == "normal":
            self.next_step()

    def refresh_stats(self):
        hearts = "♥" * self.lives + "♡" * (START_LIVES - self.lives)
        self.stats_var.set(f"Score: {self.score}    Lives: {hearts}")

    # ---------- checking answers ----------
    def submit(self, answer):
        if self.answered:
            return
        _, data = self.items[self.index]
        correct_answer = data["answer"]

        if "options" in data:
            given = answer.strip().upper()
            is_correct = given == correct_answer.upper()
        else:
            given = answer.strip().lower()
            if not given:
                self.feedback.config(text="Please type an answer first.", fg=RED)
                return
            is_correct = given == correct_answer.lower()

        self.answered = True

        if is_correct:
            self.score += 1
            self.feedback.config(text="Correct answer!", fg=GREEN)
        else:
            self.lives -= 1
            self.feedback.config(text=f"Incorrect answer. The correct answer was: {correct_answer}", fg=RED)

        # Colour the option buttons / lock the typing box
        if "options" in data:
            for letter, btn in self.option_buttons.items():
                btn.config(state="disabled")
                if letter == correct_answer.upper():
                    btn.config(bg=LIGHT_GREEN, disabledforeground="black")
                elif letter == given:
                    btn.config(bg=LIGHT_RED, disabledforeground="black")
        else:
            self.entry.config(state="disabled")
            self.submit_btn.config(state="disabled")

        self.refresh_stats()

        # Decide what the next button should say
        if self.lives == 0:
            self.next_btn.config(text="Continue")
        elif self.index + 1 >= len(self.items):
            self.next_btn.config(text="See results")
        self.next_btn.config(state="normal")
        self.bind("<Return>", lambda e: self.next_step())

    def next_step(self):
        if self.lives == 0:
            self.show_end(game_over=True)
        elif self.index + 1 >= len(self.items):
            self.show_end(game_over=False)
        else:
            self.index += 1
            self.show_question()

    # ---------- end screen ----------
    def show_end(self, game_over):
        self.clear()
        total = len(self.items)

        if game_over:
            ttk.Label(self.container, text="Game over", style="Title.TLabel").pack(pady=(50, 6))
            ttk.Label(self.container, text="You ran out of lives.", style="Sub.TLabel").pack()
        else:
            ttk.Label(self.container, text="Quiz complete!", style="Title.TLabel").pack(pady=(50, 6))
            ttk.Label(self.container, text="Well done for finishing the quiz.", style="Sub.TLabel").pack()

        ttk.Label(self.container, text=f"Final score: {self.score} / {total}",
                  font=("Segoe UI", 16, "bold")).pack(pady=20)
        ttk.Label(self.container, text="Would you like to restart?", style="Sub.TLabel").pack(pady=(0, 10))

        ttk.Button(self.container, text="Play again (same level)", style="Big.TButton", width=26,
                   command=lambda: self.start_quiz(self.level_key)).pack(pady=4)
        ttk.Button(self.container, text="Choose a different level", style="Big.TButton", width=26,
                   command=self.show_start).pack(pady=4)
        ttk.Button(self.container, text="Quit", command=self.destroy).pack(pady=(16, 0))


if __name__ == "__main__":
    QuizApp().mainloop()
