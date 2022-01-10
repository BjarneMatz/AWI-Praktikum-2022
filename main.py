from tkinter import *
from tkinter import ttk


def ex():
    exit()


root = Tk()

root.title("Hallo Welt")

mainframe = ttk.Frame(root, padding="200 200 200 200")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


ttk.Label(mainframe, text="Hallo Welt").grid(column=1, row=1)
ttk.Button(mainframe, text="Tschüss!", command=ex).grid(column=1, row=2)
root.mainloop()

# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
