import tkinter as tk
from game import game

root = tk.Tk()
root.geometry("240x220")
root.title("Life Launcher")

default_screen_width = 700
default_screen_height = 700
default_rows = 40
default_cols = 40


def start_game():
    w = h = r = c = 0
    if width_entry.get() != "":
        w = int(width_entry.get())
    if height_entry.get() != "":
        h = int(height_entry.get())
    if rows_entry.get() != "":
        r = int(rows_entry.get())
    if cols_entry.get() != "":
        c = int(cols_entry.get())

    if w == 0:
        w = default_screen_width
    elif w < 0:
        w = -w

    if h == 0:
        h = default_screen_height
    elif h < 0:
        h = -h

    if r == 0:
        r = default_rows
    elif r < 0:
        r = -r

    if c == 0:
        c = default_cols
    elif c < 0:
        c = -c
    root.withdraw()
    game(w, h, r, c)
    root.update()
    root.deiconify()


width_label = tk.Label(root, text='Screen width in pixels:')
width_label.grid(row=0, column=0, sticky='E')
width_entry = tk.Entry(root, font=('Helvetica', 12), width=10)
width_entry.grid(row=0, column=1)
width_entry.insert(0, str(default_screen_width))

height_label = tk.Label(root, text='Screen height in pixels:')
height_label.grid(row=1, column=0, sticky='E')
height_entry = tk.Entry(root, font=('Helvetica', 12), width=10)
height_entry.grid(row=1, column=1)
height_entry.insert(0, str(default_screen_height))

rows_label = tk.Label(root, text='Number of rows:')
rows_label.grid(row=2, column=0, sticky='E')
rows_entry = tk.Entry(root, font=('Helvetica', 12), width=10)
rows_entry.grid(row=2, column=1)
rows_entry.insert(0, str(default_rows))

cols_label = tk.Label(root, text='Number of columns:')
cols_label.grid(row=3, column=0, sticky='E')
cols_entry = tk.Entry(root, font=('Helvetica', 12), width=10)
cols_entry.grid(row=3, column=1)
cols_entry.insert(0, str(default_cols))

submit = tk.Button(root, text='Start Game', command=start_game)
submit.grid(row=4, column=1)

i1 = "SPACE to Pause / Unpause. While paused, press N or RIGHT to advance one stage."
i2 = "Make cell alive with left mouse, kill with right mouse. K to kill all cells. "
i3 = "Hold T to speed up advancement."

label1 = tk.Label(root, text=i1, wraplength=200, justify='left')
label2 = tk.Label(root, text=i2, wraplength=200, justify='left')
label3 = tk.Label(root, text=i3, wraplength=200, justify='left')

label1.grid(row=5, column=0, columnspan=2, sticky='W')
label2.grid(row=6, column=0, columnspan=2, sticky='W')
label3.grid(row=7, column=0, columnspan=2, sticky='W')

root.mainloop()
