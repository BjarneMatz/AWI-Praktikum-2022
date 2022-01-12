import json
import logging
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *
import requests
import re

def searchbyid():
    """this function searches for a sensor by its id"""
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

def selectdate(self, time=0):
    if self == "start":
        date = Toplevel(root)
        date.title("Select Date")
        date.geometry("600x400")
        Label(date, text="Select event start date").pack()
        cal = Calendar(date, selectmode="day")
        cal.pack()

        hour_string = ''
        min_string = ''
        sec_string = ''


        hour = ttk.Spinbox(
            date,
            from_=0,
            to=23,
            wrap=True,
            textvariable=hour_string,
            width=2,
            state="readonly",
            justify=CENTER
        )
        minute = Spinbox(
            date,
            from_=0,
            to=59,
            wrap=True,
            textvariable=min_string,
            width=2,
            justify=CENTER
        )

        second = Spinbox(
            date,
            from_=0,
            to=59,
            wrap=True,
            textvariable=sec_string,
            width=2,
            justify=CENTER
        )
        hour.pack()
        minute.pack()
        second.pack()

        h_string = hour.get()
        m_string = minute.get()
        s_string = second.get()

        if len(hour.get()) < 2:
            h_string = str(0) + hour.get()
        if len(minute.get()) < 2:
            m_string = str(0) + minute.get()
        if len(second.get()) < 2:
            s_string = str(0) + second.get()

        timestring = f"{h_string}:{m_string}:{s_string}"

        Button(date, text="Set Date", command=lambda: selectdate(cal.get_date(), timestring)).pack()
    if self == "end":
        pass
    else:
        print(self, time)
        pass



def setMeta(sensor):
    """this function sets the meta information in the sensor information frame to the current sensor used"""
    isenid.delete(0, "end")
    iurn.delete(0, "end")
    ishortname.delete(0, "end")
    ilongname.delete(0, "end")
    isenid.insert(0, sensor['id'])
    iurn.insert(0, sensor['urn'])
    ishortname.insert(0, sensor["shortName"])
    ilongname.insert(0, sensor["longName"])


def selectItem(a):
    """"this functions returns the id of the sensor selected in the treeview menu"""
    item = tw.focus()
    item = tw.item(item)
    if item["values"] == "":
        pass
    else:
        senid.delete(0, "end")
        senid.insert(0, item["values"])
        searchbyid()


def login():
    """login code by maximilian betz; used to login on sensor api service"""

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


# defining the root window
root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")

style = ttk.Style()
style.theme_use("clam")

# sensor frame is the information and select screen of the sensor
senframe = Frame(root)
senframe.place(x=0, y=0, height=360, width=640, bordermode="inside")
Label(senframe, text="Sensor Event Manager").grid(column=0, row=0)
tw = ttk.Treeview(senframe, columns="c1", cursor="hand1")
tw.place(x=0, y=25, width=200, height=330)
tw.heading(column="c1", text="Collections")

twsb = ttk.Scrollbar(senframe, orient="vertical", command=tw.yview, cursor="double_arrow")
twsb.place(x=200, y=25, width=20, height=330, anchor=NE)

collections = requests.get("https://sandbox.sensor.awi.de/rest/sensors/collections/getAllCollections")
collections = collections.json()

for ix, col in enumerate(collections):
    print(ix)
    print(col["collectionName"])
    items = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = tw.insert('', index=ix, text=col["collectionName"])
    for iix, item in enumerate(items):
        tw.insert(main, index=iix, text=item["shortName"], values=item["id"])

searchidbutton = Button(senframe, command=searchbyid, width=20, text="Search by ID")
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

# login frame
loginframe = Frame(root)
loginframe.grid(column=0, row=0)

# default button binds
tw.bind('<ButtonRelease-1>', selectItem)

finalevent = str

def geteventinfo():
    pass


startisend = ''


def samedate():
    global startisend
    print(c_samedate_state.get())
    if c_samedate_state.get() == 0:
        enddateentry.config(state=NORMAL)
        startisend = False
    if c_samedate_state.get() == 1:
        enddateentry.config(state=DISABLED)
        startisend = True

evframe = Frame(root)
evframe.place(x=640, y=0, height=720, width=640)

events = requests.get("https://sandbox.sensor.awi.de/rest/sensors/events/getAllEventTypes")
events = events.json()
clicked = StringVar()
clicked.set("Select Event")
possibevents = []

for ix, ev in enumerate(events):
    print(ix)
    print(ev["generalName"])
    possibevents.append(ev["generalName"] + " (" + str(ev["id"]) + ")")

Label(evframe, text="Event Data").place(x=0, y=0)
dd = tk.OptionMenu(evframe, clicked, *possibevents)
print(possibevents)
dd.place(x=210, y=50, width=250)

Label(evframe, text="Label").place(x=0, y=60)
Label(evframe, text="Description").place(x=0, y=85)
Label(evframe, text="Longitude").place(x=0, y=110)
Label(evframe, text="Latitude").place(x=0, y=135)
Label(evframe, text="Elevation").place(x=0, y=160)

inlabel = Entry(evframe)
inlabel.place(x=80, y=60)
indescription = Entry(evframe)
indescription.place(x=80, y=85)

#Button(evframe, text="Set Start Date", command=lambda: selectdate("start")).place(x=100, y=200)
startdateentry = Entry(evframe)
startdateentry.place(x=380, y=110, width=130)
enddateentry = Entry(evframe)
enddateentry.place(x=380, y=135, width=130)
Label(evframe, text="Start Date (format sensetive!): ").place(x=200, y=110)
Label(evframe, text="End Date (format sensetive!): ").place(x=200, y=135)
c_samedate_state = Variable()
c_samedate = Checkbutton(evframe, variable=c_samedate_state, text="Same start and end date", onvalue=1, offvalue=0, command=samedate)
c_samedate.place(x=200, y=160)
c_samedate.deselect()


upframe = Frame(root)
upframe.place(x=0, y=360, width=640, height=360)

eventdata = {
    "deviceid": "",
    "startdate": "",
    "enddate": "",
    "desctiption": "",
    "label": "",
    "eventtype": "",
    "longitude": "",
    "latitude": "",
    "elevation": ""
}

Label(upframe, text="Following data will be uploaded to SENSOR:")
Label(upframe, text="DeviceID: ")
Label(upframe, text="StartDate: ")
Label(upframe, text="EndDate ")
Label(upframe, text="Description ")
Label(upframe, text="Label: ")
Label(upframe, text="EventType ")
Label(upframe, text="Longitude: ")
Label(upframe, text="Latitude: ")
Label(upframe, text="Elevation: ")




"""
def get_eventdata():
    eventdata = {
                "itemID": sensor["id"],
                "inheritToAllChildren": "false",
                "inheritToChildren" : [],
                "event": {
                    "startDate":operation["timestamp"],
                    "endDate":operation["timestamp"],
                    "label": operation["label"],
                    "description": operation["comment"],
                    "eventType":  device_operation_ids[operation["action"]],
                    "latitude":operation["latitude"],
                    "longitude":operation["longitude"],
                    "elevationInMeter": operation["altitude"],
                    "id": None
                }
"""



root.mainloop()