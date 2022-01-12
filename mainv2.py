from tkinter import *
import tkinter as tk
from tkinter import ttk
import json
import requests
import logging


def searchById():
    "this function searches for a sensor by its id"
    with open('accounts.json', encoding='utf-8') as f:
        accounts = json.load(f)
    try:
        sid = senid.get()
        global sensor
        url = accounts['sensorurl'] + f'/sensors/device/getDevice/{sid}'
        sensor = requests.get(url)
        sensor = sensor.json()
        setMeta(sensor)
    except Exception as ex:
        print(ex)


def setMeta(sensor):
    "this function sets the meta information in the sensor information frame to the current sensor used"
    isenid.delete(0, "end")
    iurn.delete(0, "end")
    ishortname.delete(0, "end")
    ilongname.delete(0, "end")
    isenid.insert(0, sensor['id'])
    iurn.insert(0, sensor['urn'])
    ishortname.insert(0, sensor["shortName"])
    ilongname.insert(0, sensor["longName"])


def selectItem(a):
    "this functions returns the id of the sensor selected in the treeview menu"
    item = tw.focus()
    item = tw.item(item)
    if item["values"] == "":
        pass
    else:
        senid.delete(0, "end")
        senid.insert(0, item["values"])
        searchById()


def login():
    "login code by maximilian betz; used to login on sensor api service"

    with open('accounts.json', encoding='utf-8') as f:
        accounts = json.load(f)
    # Get sensor.awi.de event types access token
    try:
        # Get all device operation types and create id look up table
        url = accounts['sensorurl'] + '/sensors/events/getAllEventTypes'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Could not get AllEventTypes. {}'.format(response.text))

        device_operation_types = response.json()
        device_operation_ids = {}
        for type in device_operation_types:
            device_operation_ids[type["generalName"]] = type["id"]
        logging.info("Mapping Device Operation Type <-> ID  {}".format(device_operation_ids))

        # Get user and password from accounts.json file. Get access token and store cookie
        username = accounts['sensorawi']['user']
        password = accounts['sensorawi']['password']

        if username == "" or password == "":
            raise Exception('Sensor credentials in accounts.json mission')

        url = accounts['sensorurl'] + '/sensors/contacts/login'
        response = requests.post(url, data={
            'username': username,
            'authPassword': password
        })

        if response.status_code != 200:
            raise Exception('Could not login. {} Status code: {}'.format(response.text, response.status_code))
        token = response.cookies['x-auth-token']

    except Exception as e:
        logging.error("Communication error to sensor.awi.de: {}".format(e))




#defining the root window
root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")


#sensor frame is the information and select screen of the sensor
senframe = Frame(root)
senframe.place(x=0, y=0, height=360, width=640, bordermode="inside")
Label(senframe, text="Sensor Event Manager").grid(column=0, row=0)
tw = ttk.Treeview(senframe, columns="c1", cursor="hand1")
tw.place(x=0 ,y=25, width=200, height=330)
tw.heading(column="c1", text="Collections")

twsb = ttk.Scrollbar(senframe, orient="vertical", command=tw.yview, cursor="double_arrow")
twsb.place(x=200, y=25, width=20, height=330, anchor=NE)

collections = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/collections/getAllCollections")
collections = collections.json()

for ix, col in enumerate(collections):
    print(ix)
    print(col["collectionName"])
    items = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = tw.insert('', index=ix, text=col["collectionName"])
    for iix, item in enumerate(items):
        tw.insert(main, index=iix, text=item["shortName"], values=item["id"])

searchidbutton = Button(senframe, command=searchById, width=20, text="Search by ID")
searchidbutton.place(x=500, y=0, width=130)
senid = Entry(senframe, width=40, borderwidth=3)
senid.place(x=200, y=0, width=300)

Label(senframe, text="Data of selcted sensor").place(x=200, y=25)

Label(senframe, text="SensorID:").place(x=210, y=45)
Label(senframe, text="URN:").place(x=210, y=70)
Label(senframe, text="Shortname:").place(x=210, y=95)
Label(senframe, text="Longname:").place(x=210, y=120)

isenid = Entry(senframe)
isenid.place(x=300, y=45, width=300)
iurn = Entry(senframe)
iurn.place(x=300, y=70, width=300)
ishortname = Entry(senframe)
ishortname.place(x=300, y=95, width=300)
ilongname = Entry(senframe)
ilongname.place(x=300, y=120, width=300)

#login frame
loginframe = Frame(root)
loginframe.grid(column=0, row=0)

#default button binds
tw.bind('<ButtonRelease-1>', selectItem)

evframe = Frame(root)
evframe.place(x=360, y=0, height=640, width=360)

root.mainloop()