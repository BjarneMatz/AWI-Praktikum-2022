from tkinter import *
import tkinter as tk
from tkinter import ttk
import json
import requests
import logging

#global variables

#functions for buttons listed below
def searchById():
    try:
        sid = senid.get()
        global sensor
        sensor = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/device/getDevice/{sid}")
        sensor = sensor.json()
        setMeta()
    except Exception as ex:
        print(ex)
        pass
def setMeta():

    isenid.insert(sensor['id'])


def login():
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


root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")


#sensor frame
senframe = Frame(root)
senframe.grid(column=0, row=0)
Label(senframe, text="Sensor Event Manager").grid(column=0, row=0)

seninfo = Frame(senframe)
seninfo.grid(column=1, row=2)

senid = Entry(senframe, width=40, borderwidth=3)
senid.grid(column=1, row=0, columnspan=2)
tw = ttk.Treeview(senframe, columns="c1")
tw.grid(column=0, row=1, rowspan=3)
tw.heading(column="c1", text="Collections")

collections = requests.get(f"https://sensor.awi.de/rest/sensors/collections/getAllCollections")
collections = collections.json()

for ix, col in enumerate(collections):
    print(ix)
    print(col["collectionName"])
    items = requests.get(f"https://sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = tw.insert('', index=ix, text=col["collectionName"])
    #time.sleep(2)
    for iix, item in enumerate(items):
        tw.insert(main, index=iix, text=item["shortName"])



Button(senframe, command=searchById, width=20, text="Search by ID").grid(column=3, row=0)

Label(seninfo, text="Data of selcted sensor").grid(column=1, row=2, columnspan=2, sticky="N")

Label(seninfo, text="SensorID:").grid(column=1, row=3)
Label(seninfo, text="URN:").grid(column=1, row=4)
Label(seninfo, text="Shortname:").grid(column=1, row=5)
Label(seninfo, text="Longname:").grid(column=1, row=6)

isenid = Entry(seninfo).grid(column=2, row=3)
Entry(seninfo).grid(column=2, row=4)
Entry(seninfo).grid(column=2, row=5)
Entry(seninfo).grid(column=2, row=6)

#login frame
loginframe = Frame(root)
loginframe.grid(column=0, row=0)


root.mainloop()

