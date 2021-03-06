import tkinter as tk
from game import game
import time

root = tk.Tk()
root.geometry("240x240")
root.title("Life Launcher")
root.resizable(False, False)

default_screen_width = 420
default_screen_height = 420
default_rows = 69
default_cols = 69
entry_font = 'Helvetica'


def start_game():
    def blink(*entry):
        array = []
        for e in entry:
            if not e.get().isnumeric():
                array.append(e)
        for i in range(0, 5):
            for e in array:
                if i % 2 != 0:
                    e.config({'background': 'red2'})
                else:
                    e.config({'background': 'white'})
            time.sleep(0.20)
            root.update()

    we_good = True
    w = h = r = c = None
    if width_entry.get().isnumeric():
        w = int(width_entry.get())
        if w == 0:
            width_entry.delete(0, 'end')
            width_entry.insert(0, str(default_screen_width))
            root.update()
            w = default_screen_width
        elif w < 0:
            w = -w
    else:
        we_good = False

    if height_entry.get().isnumeric():
        h = int(height_entry.get())
        if h == 0:
            height_entry.delete(0, 'end')
            height_entry.insert(0, str(default_screen_height))
            root.update()
            h = default_screen_height
        elif h < 0:
            h = -h
    else:
        we_good = False

    if rows_entry.get().isnumeric():
        r = int(rows_entry.get())
        if r == 0:
            rows_entry.delete(0, 'end')
            rows_entry.insert(0, str(default_rows))
            root.update()
            r = default_rows
        elif r < 0:
            r = -r
    else:
        we_good = False

    if cols_entry.get().isnumeric():
        c = int(cols_entry.get())
        if c == 0:
            cols_entry.delete(0, 'end')
            cols_entry.insert(0, str(default_cols))
            root.update()
            c = default_cols
        elif c < 0:
            c = -c
    else:
        we_good = False

    if we_good:
        root.withdraw()
        game(w, h, r, c, ran.get())
        root.deiconify()
    else:
        blink(width_entry, height_entry, rows_entry, cols_entry)


# Enter Width
width_label = tk.Label(root, text='Screen width in pixels:')
width_label.grid(row=0, column=0, sticky='E')
width_entry = tk.Entry(root, font=(entry_font, 12), width=10)
width_entry.grid(row=0, column=1)
width_entry.insert(0, str(default_screen_width))

# Enter Height
height_label = tk.Label(root, text='Screen height in pixels:')
height_label.grid(row=1, column=0, sticky='E')
height_entry = tk.Entry(root, font=(entry_font, 12), width=10)
height_entry.grid(row=1, column=1)
height_entry.insert(0, str(default_screen_height))

# Enter Rows
rows_label = tk.Label(root, text='Number of rows:')
rows_label.grid(row=2, column=0, sticky='E')
rows_entry = tk.Entry(root, font=(entry_font, 12), width=10)
rows_entry.grid(row=2, column=1)
rows_entry.insert(0, str(default_rows))

# Enter Cols
cols_label = tk.Label(root, text='Number of columns:')
cols_label.grid(row=3, column=0, sticky='E')
cols_entry = tk.Entry(root, font=(entry_font, 12), width=10)
cols_entry.grid(row=3, column=1)
cols_entry.insert(0, str(default_cols))

# Randomize Checkbox
ran = tk.BooleanVar()
ran_ch_box = tk.Checkbutton(root, text='Randomize cells', variable=ran, onvalue=True, offvalue=False)
ran_ch_box.select()
ran_ch_box.grid(row=4, column=0)

# Start Game Button
start_but = tk.Button(root, text='Start Game', command=start_game)
start_but.grid(row=4, column=1)

# Instructions
i1 = "SPACE to Pause. While paused:"
i2 = "K to kill all cells. R to randomize cells. Press N or Right Arrow to advance one stage.\
 Left mouse to give cell life, right mouse to kill."
i3 = "Hold T to speed up advancement. Hold S to slow down advancement"

instruction1 = tk.Label(root, text=i1, wraplength=230, justify='left')
instruction2 = tk.Label(root, text=i2, wraplength=230, justify='left')
instruction3 = tk.Label(root, text=i3, wraplength=230, justify='left')

instruction1.grid(row=5, column=0, columnspan=3, sticky='W')
instruction2.grid(row=6, column=0, columnspan=3, sticky='W')
instruction3.grid(row=7, column=0, columnspan=3, sticky='W')


root.mainloop()
