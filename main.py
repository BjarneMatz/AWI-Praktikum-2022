from tkinter import *
import tkinter as tk


def uploadData():
    pass

def getData(sensor_id):
    pass
def viewMeta(sensor_id):
    pass

def sensorActive():
    pass

#set root window
root = tk.Tk()
root.title("SENSOR Metadata Writer")
#root.geometry("720x280")
root.config(bg="#07ace7")

#set frames of main window
header = tk.Frame(root)
footer = tk.Frame(root)
sensorinfo = tk.Frame(root)
data = tk.Frame(root)
upload = tk.Frame(root)

header.config(bg="#07acff")

sensorinfo.grid(column=0, row=0, sticky=(N, W, E, S))
data.grid(column=1, row=1, sticky=(N, W, E, S))
upload.grid(column=2, row=1, sticky=(N, W, E, S))

header.grid(column=0, row=0, sticky=(N, W, E, S))
footer.grid(column=0, row=2, sticky=(N, W, E, S))

sensorid = ttk.Frame(sensorinfo, padding="10 10 10 10").grid(column=1, row=0)
sensormeta = ttk.Frame(sensorinfo, padding="10 10 10 10").grid(column=1, row=1)



#----HEADER----
ttk.Label(header, text="SENSOR Metadata Writer").grid(column=0, row=0, sticky=(N, W, E, S))

#----SENSOR ID----
ttk.Label(sensorinfo, text="Sensor Metadata").grid(column=0, row=0, columnspan=2)
ttk.Label(sensorinfo, text="Sensor ID:").grid(column=0, row=2)
id = StringVar()
ttk.Entry(sensorinfo, width=10, text="id", textvariable=id, state=NORMAL).grid(column=1, row=2)
ttk.Button(sensorinfo, text="Load Sensor", width=30).grid(column=0, columnspan=2, row=3)

ttk.Label(sensorinfo, text="Selected Sensor:").grid(column=0, row=4, columnspan=2)
ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=5)
ttk.Label(sensorinfo, text="URN").grid(column=0, row=5)
ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=6)
ttk.Label(sensorinfo, text="Short Name").grid(column=0, row=6)
ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=1, row=7)
ttk.Label(sensorinfo, text="Long Name").grid(column=0, row=7)

ttk.Button(sensorinfo, text="view more metadata", command=viewMeta(id), state=DISABLED).grid(column=0, columnspan=2, row=8)

#----UPLOAD----
log = StringVar()
ttk.Entry(upload, textvariable=log).grid(column=1, row=2)
ttk.Button(upload, text="Upload", command=uploadData()).grid(column=1, row=1)


#----DATA INPUT----
ttk.Label(data, text="Data2Write").grid(column=1, row=0, columnspan=2)
input1 = StringVar()
ttk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=1)
ttk.Label(data, text="Data1:").grid(column=0, row=1)
input1 = StringVar()
ttk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=2)
ttk.Label(data, text="Data2:").grid(column=0, row=2)
input1 = StringVar()
ttk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=3)
ttk.Label(data, text="Data3:").grid(column=0, row=3)
input1 = StringVar()
ttk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=4)
ttk.Label(data, text="Data4:").grid(column=0, row=4)
input1 = StringVar()
ttk.Entry(data, textvariable=input1, state=DISABLED).grid(column=1, row=5)
ttk.Label(data, text="Data5:").grid(column=0, row=5)

#----FOOTER----


#main program loop
root.mainloop()