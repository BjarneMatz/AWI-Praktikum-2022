from tkinter import *
import tkinter as tk
from tkinter import ttk
import requests
import time


# set root window
root = tk.Tk()
root.title("SENSOR Metadata Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")

evframe = ttk.Frame(root)
evframe.place(x=0, y=0)
def getupdate():
    pass
def locationTop():
    pass
ti = 'time'
#ttk.Label(evframe, text="Enter event data below", style="l.Label").place(x=0, y=0)

# dropdown for possible events from api
#dd = ttk.OptionMenu(evframe, clicked, *possibevents, command=geteventtype)
#dd.place(x=80, y=50, width=400)

# input entry box description
ttk.Label(evframe, text="Label:").grid(column=0, row=1)
ttk.Label(evframe, text="Description:").place()
ttk.Label(evframe, text="Longitude:").place(x=0, y=110)
ttk.Label(evframe, text="Latitude:").place(x=250, y=160)
ttk.Label(evframe, text="Altitude:").place(x=0, y=160)

ttk.Label(evframe, text="Start Time:").grid(column=0, row=2)
ttk.Label(evframe, text="End Time:").grid(column=2, row=2)
ttk.Label(evframe, text="Attention: Format sensetive | UTC timezone").grid(column=0, columnspan=4, row=3)

# event input boxes
inlabel = ttk.Entry(evframe)
inlabel.grid(column=1, row=1, columnspan=3)
inlabel.bind("<Any-KeyPress>", getupdate)

inlongintude = ttk.Entry(evframe)
inlongintude.place(x=80, y=135)
inlongintude.bind("<Any-KeyPress>", getupdate)

inlatitude = ttk.Entry(evframe)
inlatitude.place(x=350, y=160)
inlatitude.bind("<Any-KeyPress>", getupdate)

inelevation = ttk.Entry(evframe)
inelevation.place(x=80, y=160)
inelevation.bind("<Any-KeyPress>", getupdate)

instart = ttk.Entry(evframe)
instart.grid(column=1, row=2)
instart.bind("<Any-KeyPress>", getupdate)
instart.insert(0, ti)

inend = ttk.Entry(evframe)
inend.grid(column=3, row=2)
inend.bind("<Any-KeyPress>", getupdate)
inend.insert(0, ti)

indescription = tk.Text(evframe, font=("Calibri 10"))
indescription.place(x=80, y=400, width=400, height=300)
indescription.bind("<Any-KeyPress>", getupdate)

geosearch = ttk.Entry(evframe)
geosearch.place(x=80, y=200)

ttk.Button(evframe, text="Get location by name search", command=locationTop).place(x=200, y=200)

root.mainloop()
