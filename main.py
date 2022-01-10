from tkinter import *
from tkinter import ttk


def uploadData():
    pass

def getData(sensor_id):
    pass
def viewMeta(sensor_id):
    pass

#open root window
root = Tk()
root.title("SENSOR Metadata Writer")
root.geometry("720x280")

#set frames of main window
header = ttk.Frame(root, padding="10 10 10 10")
footer = ttk.Frame(root, padding="10 10 10 10")
sensorinfo = ttk.Frame(root, padding="10 10 10 10")
eventdata = ttk.Frame(root, padding="10 10 10 10")
upload = ttk.Frame(root, padding="10 10 10 10")

sensorinfo.grid(column=0, row=1, sticky=(N, W, E, S))
eventdata.grid(column=1, row=1, sticky=(N, W, E, S))
upload.grid(column=2, row=1, sticky=(N, W, E, S))

header.grid(column=0, row=0, sticky=(N, W, E, S))
footer.grid(column=0, row=2, sticky=(N, W, E, S))

#----HEADER----
ttk.Label(header, text="SENSOR Metadata Writer").grid(column=0, row=0, sticky=(N, W, E, S))

#----SENSOR INFORMATION----
ttk.Label(sensorinfo, text="Sensor ID:").grid(column=4, row=2)
id = StringVar()
ttk.Entry(sensorinfo, width=10, text="id", textvariable=id, state=NORMAL).grid(column=5, row=2)

ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=5, row=5)
ttk.Label(sensorinfo, text="URN").grid(column=4, row=5)
ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=5, row=6)
ttk.Label(sensorinfo, text="Short Name").grid(column=4, row=6)
ttk.Entry(sensorinfo, width=20, state=DISABLED).grid(column=5, row=7)
ttk.Label(sensorinfo, text="Long Name").grid(column=4, row=7)

ttk.Button(sensorinfo, text="view more metadata", command=viewMeta(id), state=DISABLED).grid(column=4, columnspan=2, row=8)


#----FOOTER----
ttk.Button(upload, text="Upload", command=uploadData()).grid(column=1, row=2)

#main program loop
root.mainloop()