from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
curr_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")



def next_card():
    global curr_card, flip_timer
    window.after_cancel(flip_timer)
    curr_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=curr_card["French"], fill="black")
    canvas.itemconfig(card_bg, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=curr_card["English"], fill="white")
    canvas.itemconfig(card_bg, image=back_image)

def known_card():
    to_learn.remove(curr_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_button = Button(image=right_image, highlightthickness=0, command=known_card)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
right_button.grid(row=1, column=0)
wrong_button.grid(row=1, column=1)

next_card()

window.mainloop()
