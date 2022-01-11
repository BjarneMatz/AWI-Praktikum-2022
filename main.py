from tkinter import *
import tkinter as tk


def uploadData():
    pass


def getData(sensorid):
    pass


def viewMeta(sensor_id):
    pass


def sensorActive():
    pass


# set root window
root = tk.Tk()
root.title("SENSOR Metadata Writer")
# root.geometry("720x280")
root.config(bg="#07ace7")

# set frames of main window
header = tk.Frame(root)
footer = tk.Frame(root)
sensorinfo = tk.Frame(root)
data = tk.Frame(root)
upload = tk.Frame(root)

sensorinfo.grid(column=0, row=1)
data.grid(column=1, row=1)
upload.grid(column=2, row=1)

header.grid(column=0, columnspan=3, row=0)
footer.grid(column=0, row=2)

header.config(bg="#0044FF")
# ----HEADER----
tk.Label(header, text="SENSOR Metadata Writer", bg="#0044FF").grid(column=0, columnspan=3, row=0)

# ----SENSOR ID----
tk.Label(sensorinfo, text="Sensor Metadata").grid(column=0, row=0, columnspan=2)
tk.Label(sensorinfo, text="Sensor ID:").grid(column=0, row=2)
id = StringVar()
tk.Entry(sensorinfo, width=10, textvariable=id, state=NORMAL).grid(column=1, row=2)
tk.Button(sensorinfo, text="Load Sensor", width=30).grid(column=0, columnspan=2, row=3)

tk.Label(sensorinfo, text="Selected Sensor:").grid(column=0, row=4, columnspan=2)
tk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=5)
tk.Label(sensorinfo, text="URN").grid(column=0, row=5)
tk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=6)
tk.Label(sensorinfo, text="Short Name").grid(column=0, row=6)
tk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=7)
tk.Label(sensorinfo, text="Long Name").grid(column=0, row=7)

tk.Button(sensorinfo, text="view more metadata", command=viewMeta(id), state=DISABLED).grid(column=0, columnspan=2,row=8)

# ----UPLOAD----
log = StringVar()
tk.Entry(upload, textvariable=log).grid(column=1, row=2)
tk.Button(upload, text="Upload", command=uploadData()).grid(column=1, row=1)

# ----DATA INPUT----
tk.Label(data, text="Data2Write").grid(column=1, row=0, columnspan=2)
input1 = StringVar()
tk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=1)
tk.Label(data, text="Data1:").grid(column=0, row=1)
input1 = StringVar()
tk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=2)
tk.Label(data, text="Data2:").grid(column=0, row=2)
input1 = StringVar()
tk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=3)
tk.Label(data, text="Data3:").grid(column=0, row=3)
input1 = StringVar()
tk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=4)
tk.Label(data, text="Data4:").grid(column=0, row=4)
input1 = StringVar()
tk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=5)
tk.Label(data, text="Data5:").grid(column=0, row=5)

# ----FOOTER----


# main program loop
root.mainloop()
