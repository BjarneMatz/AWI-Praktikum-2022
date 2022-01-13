import json
import logging
import tkinter as tk
from tkinter import ttk
# from tkcalendar import *
import requests
# import re

# global variables
sensor = '' # sensor object from api (json)
startisend = bool

def searchbyid(event=None):
    """this function searches for a sensor by its id"""
    try:
        sid = senid.get()
        global sensor
        url = f'https://sandbox.sensor.awi.de/rest/sensors/device/getDevice/{sid}'
        sensor = requests.get(url)
        sensor = sensor.json()
        setMeta(sensor)
        getupdate()
    except ValueError as ex:
       x = "Input outside of search zone"
       errorwin(x)

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


def selectItem(a=None):
    """"this functions returns the id of the sensor selected in the treeview menu"""
    i = tw.focus()
    i = tw.item(i)
    if i["values"] == "":
        pass
    else:
        senid.delete(0, "end")
        senid.insert(0, i["values"])
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




def getupdate(a=None):
    try:
        eventdata["deviceid"] = str(sensor["id"])
    except Exception as ex:
        print(ex)
    try:
        eventdata["desctiption"] = indescription.get(0, tk.END)
    except Exception as ex:
        print(ex)
    try:
        eventdata["longitude"] = inlongintude.get()
    except Exception as ex:
        print(ex)
    try:
        eventdata["latitude"] = inlatitude.get()
    except Exception as ex:
        print(ex)
    try:
        eventdata["elevation"] = inelevation.get()
    except Exception as ex:
        print(ex)
    try:
        eventdata["label"] = inlabel.get()
    except Exception as ex:
        print(ex)
    try:
        updateuploadinfo()
    except Exception as ex:
        print(ex)

def updateuploadinfo():
    upid.delete(0, tk.END)
    upid.insert(0, eventdata["deviceid"])
def errorwin(error):
    errwin = tk.Toplevel()
    errwin.resizable(False, False)
    err = ttk.Frame(errwin)
    err.place(x=0, y=0, width=4000, height=2000)
    ttk.Label(errwin, text="Error:", font="Calibri 20").place(x=0, y=0)
    ttk.Label(errwin, text=error, font="Calibri 12").place(x=0, y=30)
    ttk.Button(errwin, text="OK", command=errwin.destroy).place(x=50, y=100)

# defining the root window

root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")

style = ttk.Style()
style.theme_use("clam")

# sensor frame is the information and select screen of the sensor

senframe = ttk.Frame(root)
senframe.place(x=0, y=0, height=360, width=640, bordermode="inside")

ttk.Label(senframe, text="Sensor Event Manager").grid(column=0, row=0)

tw = ttk.Treeview(senframe, columns="c1", cursor="hand1")
tw.place(x=0, y=25, width=200, height=330)
tw.heading(column="c1", text="Collections")

#scrollbar for treeview
twsb = ttk.Scrollbar(senframe, orient="vertical", command=tw.yview, cursor="double_arrow")
twsb.place(x=200, y=25, width=20, height=330, anchor="ne")




searchidbutton = ttk.Button(senframe, command=searchbyid, width=20, text="Search by ID")
searchidbutton.place(x=500, y=0, width=130)

senid = ttk.Entry(senframe, width=40)
senid.place(x=200, y=0, width=300)
senid.bind("<Return>", func=searchbyid)

# meta information about selected sensor
ttk.Label(senframe, text="Data of selcted sensor").place(x=200, y=25)
ttk.Label(senframe, text="SensorID:").place(x=210, y=45)
ttk.Label(senframe, text="URN:").place(x=210, y=70)
ttk.Label(senframe, text="Shortname:").place(x=210, y=95)
ttk.Label(senframe, text="Longname:").place(x=210, y=120)


isenid = ttk.Entry(senframe)
isenid.place(x=300, y=45, width=300)
iurn = ttk.Entry(senframe)
iurn.place(x=300, y=70, width=300)
ishortname = ttk.Entry(senframe)
ishortname.place(x=300, y=95, width=300)
ilongname = ttk.Entry(senframe)
ilongname.place(x=300, y=120, width=300)

# make it possible to select items in treeview menu
tw.bind('<ButtonRelease-1>', selectItem)

# get all collections through api
collections = requests.get("https://sandbox.sensor.awi.de/rest/sensors/collections/getAllCollections")
collections = collections.json()

for ix, col in enumerate(collections):
    print(ix)
    print(col["collectionName"])
    #get sensors from api
    items = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = tw.insert('', index=ix, text=col["collectionName"])
    for iix, item in enumerate(items):
        tw.insert(main, index=iix, text=item["shortName"], values=item["id"])

"""
# part of old time picker; maybe reusable

def samedate():
global startisend
print(c_samedate_state.get())
if c_samedate_state.get() == 0:
    enddateentry.config(state="NORMAL")
    startisend = False
if c_samedate_state.get() == 1:
    enddateentry.config(state=tk.DISABLED)
    startisend = True
"""

# event input frame
evframe = ttk.Frame(root)
evframe.place(x=640, y=0, height=720, width=640)

# get all possible events from api
events = requests.get("https://sandbox.sensor.awi.de/rest/sensors/events/getAllEventTypes")
events = events.json()
clicked = tk.StringVar()
clicked.set("Select Event")
possibevents = []
for ix, ev in enumerate(events):
    print(ix)
    print(ev["generalName"])
    possibevents.append(ev["generalName"] + " (" + str(ev["id"]) + ")")
ttk.Label(evframe, text="Event Data").place(x=0, y=0)


#dropdown for possible events from api
dd = ttk.OptionMenu(evframe, clicked, *possibevents)
dd.place(x=210, y=50, width=250)

# input entry box description
ttk.Label(evframe, text="Label:").place(x=0, y=60)
ttk.Label(evframe, text="Description:").place(x=0, y=200)
ttk.Label(evframe, text="Longitude:").place(x=0, y=110)
ttk.Label(evframe, text="Latitude:").place(x=0, y=135)
ttk.Label(evframe, text="Elevation:").place(x=0, y=160)


#event input boxes
inlabel = ttk.Entry(evframe)
inlabel.place(x=80, y=60)
inlongintude = ttk.Entry(evframe)
inlongintude.place(x=80, y=110)
inlatitude = ttk.Entry(evframe)
inlatitude.place(x=80, y=135)
inelevation = ttk.Entry(evframe)
inelevation.place(x=80, y=160)

indescription = tk.Text(evframe, font=("Calibri 10"))
indescription.place(x=80, y=200, width=400, height=300)
indescription.bind("<Any-KeyPress>", getupdate)
"""
# old time function; maybe reusable

Button(evframe, text="Set Start Date", command=lambda: selectdate("start")).place(x=100, y=200)
startdateentry = ttk.Entry(evframe)
startdateentry.place(x=380, y=110, width=130)
enddateentry = ttk.Entry(evframe)
enddateentry.place(x=380, y=135, width=130)
ttk.Label(evframe, text="Start Date (format sensetive!): ").place(x=200, y=110)
ttk.Label(evframe, text="End Date (format sensetive!): ").place(x=200, y=135)
c_samedate_state = tk.Variable()
c_samedate = ttk.Checkbutton(evframe, variable=c_samedate_state, text="Same start and end date", onvalue=1, offvalue=0, command=samedate)
c_samedate.place(x=200, y=160)
#c_samedate.deselect()
"""

upframe = ttk.Frame(root)
upframe.place(x=0, y=360, width=640, height=360)
upid = ttk.Entry(upframe)

ttk.Label(upframe, text="Following data will be uploaded to SENSOR:").place(x=0, y=0)
ttk.Label(upframe, text="DeviceID: ").place(x=0, y=25)
ttk.Label(upframe, text="StartDate: ").place(x=0, y=50)
ttk.Label(upframe, text="EndDate: ").place(x=0, y=75)
ttk.Label(upframe, text="Description: ").place(x=0, y=100)
ttk.Label(upframe, text="Label: ").place(x=0, y=125)
ttk.Label(upframe, text="EventType: ").place(x=0, y=150)
ttk.Label(upframe, text="Longitude: ").place(x=0, y=175)
ttk.Label(upframe, text="Latitude: ").place(x=0, y=200)
ttk.Label(upframe, text="Elevation: ").place(x=0, y=225)


upid.place(x=75, y=25, width=300)
upstart = ttk.Entry(upframe, state=tk.DISABLED)
upstart.place(x=75, y=50, width=300)
upend = ttk.Entry(upframe)
upend.place(x=75, y=75, width=300)
updesc = ttk.Entry(upframe)
updesc.place(x=75, y=100, width=300)
uplab = ttk.Entry(upframe)
uplab.place(x=75, y=125, width=300)
uptype = ttk.Entry(upframe)
uptype.place(x=75, y=150, width=300)
uplong = ttk.Entry(upframe)
uplong.place(x=75, y=175, width=300)
uplat = ttk.Entry(upframe)
uplat.place(x=75, y=200, width=300)
upel = ttk.Entry(upframe)
upel.place(x=75, y=225, width=300)

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