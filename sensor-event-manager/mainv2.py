import datetime
import json
import logging
import tkinter as tk
from tkinter import ttk

from geopy.geocoders import Nominatim

geolocation = Nominatim(user_agent="SENSOR-Event-Manger")

import requests

ti = str(datetime.datetime.utcnow())
ti = ti[0:10] + "T" + ti[11:19]

# import re

# global variables
sensor = ''  # sensor object from api (json)
startisend = bool
eventtypefromdd = ''
token = ''


def getLocation(a=None):
    try:
        global geosearch
        global locinfo
        location = geolocation.geocode(geosearch.get())
        print(location.address)
        inlongintude.delete(0, "end")
        inlatitude.delete(0, "end")
        inelevation.delete(0, "end")
        locinfo.delete('1.0', "end")
        inlongintude.insert(0, location.longitude)
        inlatitude.insert(0, location.latitude)
        inelevation.insert(0, location.altitude)
        locinfo.insert('1.0', location.address)
    except Exception as ex:
        print(ex)
        locinfo.delete("1.0", "end")
        locinfo.insert("1.0", "Error: Timeout / Location can not be found")


def locationTop():
    global geosearch
    global locinfo
    loca = tk.Toplevel()
    loc = ttk.Frame(loca)
    loc.pack()
    ttk.Label(loc, text="Search location by name").grid(column=0, row=0, columnspan=3)
    ttk.Label(loc, text="Enter Location Name:").grid(column=0, row=1)
    locinfo = tk.Text(loc, width=50, height=10)
    locinfo.grid(column=0, row=3, columnspan=3)
    geosearch = ttk.Entry(loc, width=30)
    geosearch.grid(column=1, row=1)
    search_button = ttk.Button(loc, command=getLocation, text="Get Location")
    search_button.grid(column=0, row=4, columnspan=2)
    geosearch.bind("<Return>", getLocation)
    search_button.bind("<Return>", getLocation)


def geteventtype(a=None):
    global eventtypefromdd
    eventtypefromdd = int(''.join(list(filter(str.isdigit, clicked.get()))))


def searchbyid(a=None):
    """this function searches for a sensor by its id"""
    try:
        sid = senid.get()
        global sensor
        url = f'https://sandbox.sensor.awi.de/rest/sensors/device/getDevice/{sid}'
        sensor = requests.get(url)
        sensor = sensor.json()
        setMeta(sensor)
        getupdate()
    except ValueError:
        x = "Input outside of search zone"
        errorwin(x)


def setMeta(a):
    """this function sets the meta information in the sensor information frame to the current sensor used"""

    isenid.config(state=tk.NORMAL)
    iurn.config(state=tk.NORMAL)
    ishortname.config(state=tk.NORMAL)
    ilongname.config(state=tk.NORMAL)
    isenid.delete(0, "end")
    iurn.delete(0, "end")
    ishortname.delete(0, "end")
    ilongname.delete(0, "end")
    isenid.insert(0, a['id'])
    iurn.insert(0, a['urn'])
    ishortname.insert(0, a["shortName"])
    ilongname.insert(0, a["longName"])
    isenid.config(state=tk.DISABLED)
    iurn.config(state=tk.DISABLED)
    ishortname.config(state=tk.DISABLED)
    ilongname.config(state=tk.DISABLED)


def selectItem(a=None):
    """"this functions returns the id of the sensor selected in the treeview menu"""
    i = tw.focus()
    h = tw.item(i)

    if h["values"] == "":
        pass
    else:
        senid.delete(0, "end")
        senid.insert(0, h["values"])
        if tw.get_children(i):
            pass
        else:
            childs = requests.get(
                f"https://sandbox.sensor.awi.de/rest/sensors/device/getChildrenOfDevice/{senid.get()}")
            childs = childs.json()
            for iiix, child in enumerate(childs):
                tw.insert(i, index=iiix, text=child["shortName"], values=child["id"])  #
                print(child["shortName"])
        searchbyid()


def login():
    """login code by maximilian betz; used to login on sensor api service"""
    global token
    with open('accounts.json', encoding='utf-8') as f:
        accounts = json.load(f)
    # Get sensor.awi.de event types access token
    try:
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
            errorwin("Login to SENSOR.awi.de failed.")
            raise Exception('Could not login. {} Status code: {}'.format(response.text, response.status_code))
        else:
            print("Login Successful")
        token = response.cookies['x-auth-token']

    except Exception as e:
        logging.error("Communication error to sensor.awi.de: {}".format(e))


def getupdate(a=None):
    # get current data from entry boxes and save in dictonary
    eventdata["deviceid"] = isenid.get()
    eventdata["description"] = indescription.get(1.0, "end")
    eventdata["longitude"] = inlongintude.get()
    eventdata["latitude"] = inlatitude.get()
    eventdata["altitude"] = inelevation.get()
    eventdata["label"] = inlabel.get()
    eventdata["deviceid"] = senid.get()
    eventdata["startdate"] = instart.get()
    eventdata["enddate"] = inend.get()
    eventdata["eventtype"] = eventtypefromdd
    print(eventdata)


def errorwin(error):
    """function for creating error message boxes"""
    errwin = tk.Toplevel()
    errwin.resizable(False, False)
    errwin.geometry("1260x200")
    err = ttk.Frame(errwin)
    err.place(x=0, y=0, width=4000, height=2000)
    ttk.Label(errwin, text="Error:", font="Calibri 20").pack()
    ttk.Label(errwin, text=error, font="Calibri 12").pack()
    ttk.Button(errwin, text="OK", command=errwin.destroy).pack()


def upload():
    """Here the data gets actually uploaded via api"""
    uploaddata = {
        "itemID": eventdata['deviceid'],
        "inheritToAllChildren": True,
        "inheritToChildren": [
            0
        ],
        "event": {
            "startDate": f"{eventdata['startdate']}",
            "endDate": f"{eventdata['enddate']}",
            "label": f"{eventdata['label']}",
            "description": f"{eventdata['description']}",
            "eventType": eventdata["eventtype"],
            "longitude": eventdata['longitude'],
            "latitude": eventdata['latitude'],
            "elevationInMeter": eventdata["altitude"],
            "id": None
        }
    }
    headers = {"Content-Type": "application/json"}
    url = f"https://sandbox.sensor.awi.de/rest/sensors/events/putEvent/{eventdata['deviceid']}?createVersion=false"
    response = requests.put(url, data=json.dumps(uploaddata), headers=headers, cookies={'x-auth-token': token})
    print(token)
    print(url)
    print(headers)
    print(json.dumps(uploaddata))
    print(response)
    if response.status_code != 201:
        errorwin("Transfer to SENSOR.awi.de FAILED!")
        raise Exception("Transfer to SENSOR.awi.de FAILED!")
    else:
        cwin.destroy()
        fine = tk.Toplevel(root)
        fine.title("Upload Successful")
        fine.geometry("500x100")
        fine_frame = ttk.Frame(fine)
        fine_frame.place(x=0, y=0, width=500, height=500)
        ttk.Label(fine_frame, text="Upload Successful!", font=("Calibri", 30)).pack()
        ttk.Button(fine_frame, text="Ok", command=fine.destroy).pack()


def confirm():
    """Function to open a confirm window on upload begin"""
    global cwin
    getupdate()
    cwin = tk.Toplevel(root)
    cwin.geometry("700x500")
    cframe = ttk.Frame(cwin)
    cframe.place(x=0, y=0, width=1000, height=1000)
    ttk.Label(cframe, text="You are about to upload following action to SENSOR.awi.de").place(x=0, y=0)
    ttk.Label(cframe, text=f"DeviceID: {eventdata['deviceid']}").place(x=0, y=30)
    ttk.Label(cframe, text=f"Label: {eventdata['label']}").place(x=0, y=60)
    ttk.Label(cframe, text=f"Start Date: {eventdata['startdate']}").place(x=0, y=90)
    ttk.Label(cframe, text=f"End Date: {eventdata['enddate']}").place(x=0, y=120)
    ttk.Label(cframe, text=f"Event Type: {eventdata['eventtype']}").place(x=0, y=150)
    ttk.Label(cframe, text=f"Longitude: {eventdata['longitude']}").place(x=0, y=180)
    ttk.Label(cframe, text=f"Latitude: {eventdata['latitude']}").place(x=0, y=210)
    ttk.Label(cframe, text=f"Altitude: {eventdata['altitude']}").place(x=0, y=240)
    ttk.Label(cframe, text=f"Description: {eventdata['description']}").place(x=0, y=270)
    ttk.Label(cframe,
              text="Please be aware that this action can't be undone by this program and need to be undone through the web interface.").place(
        x=0, y=430)

    ttk.Button(cframe, text="Im sure, go upload", command=upload).place(x=300, y=450)
    ttk.Button(cframe, text="STOP", command=cwin.destroy).place(x=200, y=450)


###################################################################################

# defining the root window
root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")
root.resizable(False, False)
style = ttk.Style()
style.theme_use("clam")

# information and selection of sensor
senframe = ttk.Frame(root)
senframe.place(x=0, y=0, height=360, width=640, bordermode="inside")

ttk.Label(senframe, text="Sensor Event Manager").place(x=0, y=0)

tw = ttk.Treeview(senframe)
tw.place(x=0, y=25, width=200, height=330)

# scrollbar for treeview
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
    # get sensors from api
    items = requests.get(f"https://sandbox.sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
    items = items.json()
    main = tw.insert('', index=ix, text=col["collectionName"])
    for iix, item in enumerate(items):
        childinsert = tw.insert(main, index=iix, text=item["shortName"], values=item["id"])

# event input frame
evframe = ttk.Frame(root)
evframe.place(x=640, y=0, height=720, width=640)

# get all possible events from api
events = requests.get("https://sandbox.sensor.awi.de/rest/sensors/events/getAllEventTypes")
events = events.json()
clicked = tk.StringVar()
clicked.set("Select Event")
possibevents = []
possibevents.append("Select Event")
for ix, ev in enumerate(events):
    print(ix)
    print(ev["generalName"])
    possibevents.append(ev["generalName"] + " (" + str(ev["id"]) + ")")
ttk.Style.configure(style, "l.Label", font=(None, 20))
ttk.Label(evframe, text="Enter event data below", style="l.Label").place(x=0, y=0)

# dropdown for possible events from api
dd = ttk.OptionMenu(evframe, clicked, *possibevents, command=geteventtype)
dd.place(x=80, y=50, width=400)

# input entry box description
ttk.Label(evframe, text="Label:").place(x=0, y=85)
ttk.Label(evframe, text="Description:").place(x=0, y=300)
ttk.Label(evframe, text="Longitude:").place(x=0, y=160)
ttk.Label(evframe, text="Latitude:").place(x=250, y=160)
ttk.Label(evframe, text="Altitude:").place(x=0, y=185)
ttk.Label(evframe, text="Start Time:").place(x=0, y=110)
ttk.Label(evframe, text="End Time:").place(x=250, y=110)
ttk.Label(evframe, text="Attention: Format sensetive | UTC timezone").place(x=80, y=135)

# event input boxes
inlabel = ttk.Entry(evframe)
inlabel.place(x=80, y=85, width=400)

inlongintude = ttk.Entry(evframe)
inlongintude.place(x=80, y=160)

inlatitude = ttk.Entry(evframe)
inlatitude.place(x=350, y=160)

inelevation = ttk.Entry(evframe)
inelevation.place(x=80, y=185)

instart = ttk.Entry(evframe)
instart.place(x=80, y=110)
instart.insert(0, ti)

inend = ttk.Entry(evframe)
inend.place(x=350, y=110)
inend.insert(0, ti)

ttk.Button(evframe, text="Get location by name search", command=locationTop).place(x=80, y=210, width=400)

indescription = tk.Text(evframe, font=("Calibri 10"))
indescription.place(x=80, y=300, width=400, height=300)


# frame bottom left, simply holds upload button in place
upframe = ttk.Frame(root)
upframe.place(x=0, y=360, width=640, height=360)
ttk.Button(upframe, text="Upload to SENSOR", command=confirm, style="b.TButton").place(x=30, y=30, width=500, height=250)
ttk.Style.configure(style, "b.TButton", font=(None, 30))

# event data dictionary that holds data until upload
eventdata = {
    "deviceid": "",
    "startdate": "",
    "enddate": "",
    "description": "",
    "label": "",
    "eventtype": "",
    "longitude": "",
    "latitude": "",
    "altitude": ""
}

#login to sensor.awi.de on program startup
login()
#main program loop
root.mainloop()
