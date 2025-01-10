# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:32:48 2024

@author: Asus
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

class TypingTestGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test Game")
        self.root.geometry("800x600")
        self.level = None
        self.start_time = None
        self.end_time = None
        self.texts = {
            'beginner': 'The quick brown fox jumps over the lazy dog.',
            'intermediate': 'She sells sea shells by the sea shore.',
            'advanced': 'A quick movement of the enemy will jeopardize six gunboats.'
        }

        self.create_widgets()

    def create_widgets(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.add_background(self.start_frame, r"D:\start_background.jpg")

        tk.Label(self.start_frame, text="Welcome to the Typing Test Game!", font=("Helvetica", 24), bg='#ffcccb').pack(pady=30)
        self.start_button = tk.Button(self.start_frame, text="Start", command=self.show_level_selection, font=("Helvetica", 18), bg='#ffcccb')
        self.start_button.pack(pady=20)

    def add_background(self, frame, image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((800, 600), Image.BILINEAR)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(frame, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

    def show_level_selection(self):
        self.start_frame.pack_forget()

        self.level_frame = tk.Frame(self.root)
        self.level_frame.pack(fill=tk.BOTH, expand=True)
        self.add_background(self.level_frame, r"D:\level_background.jpg")

        tk.Label(self.level_frame, text="Select Level:", font=("Helvetica", 22), bg='#ffcccb').pack(pady=20)
        tk.Button(self.level_frame, text="Beginner", command=lambda: self.show_level_description('beginner'), font=("Helvetica", 16), bg='#ffcccb').pack(pady=10)
        tk.Button(self.level_frame, text="Intermediate", command=lambda: self.show_level_description('intermediate'), font=("Helvetica", 16), bg='#ffcccb').pack(pady=10)
        tk.Button(self.level_frame, text="Advanced", command=lambda: self.show_level_description('advanced'), font=("Helvetica", 16), bg='#ffcccb').pack(pady=10)

    def show_level_description(self, level):
        descriptions = {
            'beginner': 'Beginner: Simple sentences with common words.',
            'intermediate': 'Intermediate: Tongue twisters and moderate difficulty sentences.',
            'advanced': 'Advanced: Complex sentences with uncommon words.'
        }
        messagebox.showinfo("Level Description", descriptions[level])
        self.level_frame.pack_forget()
        self.start_test(level)

    def start_test(self, level):
        self.level = level
        self.start_time = time.time()

        self.test_text = self.texts[level]
        self.typed_text = tk.StringVar()

        self.test_frame = tk.Frame(self.root)
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        self.add_background(self.test_frame, r"D:\test_background.jpg")

        tk.Label(self.test_frame, text="Type the following text:", font=("Helvetica", 18), bg='#ffcccb').pack(pady=20)
        self.text_label = tk.Label(self.test_frame, text=self.test_text, wraplength=700, justify='left', font=("Helvetica", 16), bg='#ffcccb')
        self.text_label.pack(pady=10)

        self.input_entry = tk.Entry(self.test_frame, textvariable=self.typed_text, width=60, font=("Helvetica", 16))
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<KeyRelease>', self.update_text_display)
        self.input_entry.bind('<Return>', self.check_result)
        self.input_entry.focus_set()

        self.timer_label = tk.Label(self.test_frame, text="Time: 0.00 seconds", font=("Helvetica", 16), bg='#ffcccb')
        self.timer_label.pack(pady=10)
        self.update_timer()

    def update_text_display(self, event=None):
        typed = self.typed_text.get()
        correct_part = self.test_text[:len(typed)]
        wrong_part = self.test_text[len(typed):]

        self.text_label.config(text=f"{correct_part}{wrong_part}")

    def update_timer(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed_time:.2f} seconds")
        self.root.after(100, self.update_timer)

    def check_result(self, event=None):
        self.end_time = time.time()
        typed = self.typed_text.get()

        self.test_frame.pack_forget()

        elapsed_time = self.end_time - self.start_time
        correct = typed.strip() == self.test_text.strip()
        accuracy = sum(1 for a, b in zip(typed, self.test_text) if a == b) / len(self.test_text) * 100

        result_text = f"Time: {elapsed_time:.2f} seconds\nAccuracy: {accuracy:.2f}%\n"
        result_text += "Correct!" if correct else "Incorrect."
        result_text += "\nYou need more practice." if not correct or accuracy < 90 else "\nYou aced the test!"

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        if not correct or accuracy < 90:
            self.add_background(self.result_frame, r"D:\try_again.jpg.jpg")
        else:
            self.add_background(self.result_frame, r"D:\keep_going.jpg")
        tk.Label(self.result_frame, text=result_text, font=("Helvetica", 18), bg='#ffcccb').pack(pady=20)
        tk.Button(self.result_frame, text="Try Again", command=self.retry, font=("Helvetica", 16), bg='#ffcccb').pack(side=tk.LEFT, padx=30, pady=20)
        tk.Button(self.result_frame, text="End Game", command=self.root.quit, font=("Helvetica", 16), bg='#ffcccb').pack(side=tk.RIGHT, padx=30, pady=20)

    def retry(self):
        self.result_frame.pack_forget()
        self.show_level_selection()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestGame(root)
    root.mainloop()
