from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
import time



def uploadData():
    pass


def getData():
    try:
        sid = id.get()
        sensor = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/device/getDevice/{sid}")
        sensor = sensor.json()
        urnget = sensor["urn"]
        shortnameget = sensor["shortName"]
        longnameget = sensor["longName"]


        changeText(urn, urnget)
        changeText(shortname, shortnameget)
        changeText(longname, longnameget)
        metabutton.config(state=NORMAL)
    except Exception as ex:
        changeText(logger, ex)

def changeText(box, string):
    box.config(state=NORMAL)
    box.insert(0, string)
    box.config(state=DISABLED)
def viewMeta():
    pass


def sensorActive():
    pass


# set root window
root = tk.Tk()
root.title("SENSOR Metadata Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")

# set frames of main window
header = tk.Frame(root)
footer = tk.Frame(root)
sensorinfo = tk.Frame(root)
data = tk.Frame(root)
upload = tk.Frame(root)
sensorlib = tk.Frame(root)

sensorinfo.grid(column=0, row=1)
data.grid(column=1, row=1)
upload.grid(column=2, row=1)
sensorlib.grid(column=3, row=1)

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
tk.Button(sensorinfo, text="Load Sensor", width=30, command=getData).grid(column=0, columnspan=2, row=3)

tk.Label(sensorinfo, text="Selected Sensor:").grid(column=0, row=4, columnspan=2)
urn = tk.Entry(sensorinfo, width=80, state=DISABLED)
urn.grid(column=1, row=5)
tk.Label(sensorinfo, text="URN").grid(column=0, row=5)
shortname = tk.Entry(sensorinfo, width=80, state=DISABLED)
shortname.grid(column=1, row=6)
tk.Label(sensorinfo, text="Short Name").grid(column=0, row=6)
longname = tk.Entry(sensorinfo, width=80, state=DISABLED)
longname.grid(column=1, row=7)
tk.Label(sensorinfo, text="Long Name").grid(column=0, row=7)

metabutton = tk.Button(sensorinfo, text="view more metadata", command=viewMeta, state=DISABLED)
metabutton.grid(column=0, columnspan=2,row=8)

# ----UPLOAD----
log = StringVar()
logger = tk.Entry(upload, state=DISABLED)
logger.grid(column=1, row=2)
tk.Button(upload, text="Upload", command=uploadData).grid(column=1, row=1)


# ----TREE SENSOR LIBRARY----
twc = ttk.Treeview(sensorlib)
twc.pack()



collections = requests.get(f"https://sensor.awi.de/rest/sensors/collections/getAllCollections")
collections = collections.json()



for ix, col in enumerate(collections):
    print(ix)
    print(col["collectionName"])
    items = requests.get(f"https://sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = twc.insert('', iid=ix, index=ix, text=col["collectionName"])
    #time.sleep(2)
    for iix, item in enumerate(items):
        twc.insert(main, index=iix, text=item["shortName"])




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
