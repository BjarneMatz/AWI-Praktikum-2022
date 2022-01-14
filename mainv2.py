import datetime
import json
import logging
import requests
import tkinter as tk
from tkinter import ttk

ti = str(datetime.datetime.utcnow())
ti = ti[0:10] + "T"+ ti[11:19]


# import re

# global variables
sensor = ''  # sensor object from api (json)
startisend = bool
eventtypefromdd = ''
token = ''
def geteventtype(self):
    global eventtypefromdd
    eventtypefromdd = int(''.join(list(filter(str.isdigit, clicked.get()))))

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

    isenid.config(state=tk.NORMAL)
    iurn.config(state=tk.NORMAL)
    ishortname.config(state=tk.NORMAL)
    ilongname.config(state=tk.NORMAL)
    isenid.delete(0, "end")
    iurn.delete(0, "end")
    ishortname.delete(0, "end")
    ilongname.delete(0, "end")
    isenid.insert(0, sensor['id'])
    iurn.insert(0, sensor['urn'])
    ishortname.insert(0, sensor["shortName"])
    ilongname.insert(0, sensor["longName"])
    isenid.config(state=tk.DISABLED)
    iurn.config(state=tk.DISABLED)
    ishortname.config(state=tk.DISABLED)
    ilongname.config(state=tk.DISABLED)



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
    global token
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
            errorwin("Login to SENSOR.awi.de failed.")
            raise Exception('Could not login. {} Status code: {}'.format(response.text, response.status_code))
        else:
            print("Login Successful")
        token = response.cookies['x-auth-token']

    except Exception as e:
        logging.error("Communication error to sensor.awi.de: {}".format(e))


def getupdate(a=None):
    # get current data from entry boxes and save in dictonary
    eventdata["deviceid"] = senid.get()
    eventdata["description"] = indescription.get(1.0, "end")
    eventdata["longitude"] = inlongintude.get()
    eventdata["latitude"] = inlatitude.get()
    eventdata["altitude"] = inelevation.get()
    eventdata["label"] = inlabel.get()
    eventdata["deviceid"] = senid.get()
    eventdata["startdate"] = instart.get()
    eventdata["enddate"] = inend.get()
    eventdata["eventtype"] = eventtypefromdd


"""
def updateuploadinfo():
    upid.delete(0, tk.END)
    upid.insert(0, eventdata["deviceid"])
    updesc.delete(0, tk.END)
    updesc.insert(0, eventdata["desctiption"])
    uplong.delete(0, "end")
    uplong.insert(0, eventdata["longitude"])
    uplat.delete(0, tk.END)
    uplat.insert(0, eventdata["latitude"])
    uplab.delete(0, "end")
    uplab.insert(0, eventdata["label"])
    upel.delete(0, "end")
    upel.insert(0, eventdata["altitude"])
    uptype.delete(0, tk.END)
    uptype.insert(0, eventdata["eventtype"])
"""

def errorwin(error):
    """function for creating error message boxes"""
    errwin = tk.Toplevel()
    errwin.resizable(False, False)
    err = ttk.Frame(errwin)
    err.place(x=0, y=0, width=4000, height=2000)
    ttk.Label(errwin, text="Error:", font="Calibri 20").place(x=0, y=0)
    ttk.Label(errwin, text=error, font="Calibri 12").place(x=0, y=30)
    ttk.Button(errwin, text="OK", command=errwin.destroy).place(x=50, y=100)
def upload():
    """Here the data gets actually uploaded via api"""
    pass
def confirm():
    """Function to open a confirm window on upload begin"""
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
    ttk.Label(cframe, text="Please be aware that this action can't be undone by this program and need to be undone through the web interface").place(x=0, y=430)

    ttk.Button(cframe, text="Im sure, go upload", command=upload).place(x=300, y=450)
    ttk.Button(cframe, text="STOP", command=cwin.destroy).place(x=200, y=450)

    pass
# defining the root window
root = tk.Tk()
root.title("Event Writer")
root.geometry("1280x720")
root.config(bg="#07ace7")
style = ttk.Style()
style.theme_use("clam")

# information and selection of sensor
senframe = ttk.Frame(root)
senframe.place(x=0, y=0, height=360, width=640, bordermode="inside")

ttk.Label(senframe, text="Sensor Event Manager").grid(column=0, row=0)

tw = ttk.Treeview(senframe, columns="c1", cursor="hand1")
tw.place(x=0, y=25, width=200, height=330)
tw.heading(column="c1", text="Collections")

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
ttk.Label(evframe, text="Description:").place(x=0, y=200)
ttk.Label(evframe, text="Longitude:").place(x=0, y=110)
ttk.Label(evframe, text="Latitude:").place(x=0, y=135)
ttk.Label(evframe, text="Altitude:").place(x=0, y=160)

ttk.Label(evframe, text="Start Time:").place(x=250, y=110)
ttk.Label(evframe, text="End Time:").place(x=250, y=135)
ttk.Label(evframe, text="Attention: Format sensetive | UTC timezone").place(x=250, y=160)

# event input boxes
inlabel = ttk.Entry(evframe)
inlabel.place(x=80, y=85)
inlabel.bind("<Any-KeyPress>", getupdate)

inlongintude = ttk.Entry(evframe)
inlongintude.place(x=80, y=110)
inlongintude.bind("<Any-KeyPress>", getupdate)

inlatitude = ttk.Entry(evframe)
inlatitude.place(x=80, y=135)
inlatitude.bind("<Any-KeyPress>", getupdate)

inelevation = ttk.Entry(evframe)
inelevation.place(x=80, y=160)
inelevation.bind("<Any-KeyPress>", getupdate)

instart = ttk.Entry(evframe)
instart.place(x=350, y=110)
instart.bind("<Any-KeyPress>", getupdate)
instart.insert(0, ti)

inend = ttk.Entry(evframe)
inend.place(x=350, y=135)
inend.bind("<Any-KeyPress>", getupdate)
inend.insert(0, ti)



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

ttk.Button(upframe, text="Upload to SENSOR", command=confirm, style="b.TButton").place(x=30, y=30, width=500, height=250)
ttk.Style.configure(style, "b.TButton", font=(None, 30))


"""
ttk.Label(upframe, text="Following data will be uploaded to SENSOR:").place(x=0, y=0)
ttk.Label(upframe, text="DeviceID: ").place(x=0, y=25)
ttk.Label(upframe, text="StartDate: ").place(x=0, y=50)
ttk.Label(upframe, text="EndDate: ").place(x=0, y=75)
ttk.Label(upframe, text="Description: ").place(x=0, y=100)
ttk.Label(upframe, text="Label: ").place(x=0, y=125)
ttk.Label(upframe, text="EventType: ").place(x=0, y=150)
ttk.Label(upframe, text="Longitude: ").place(x=0, y=175)
ttk.Label(upframe, text="Latitude: ").place(x=0, y=200)
ttk.Label(upframe, text="Altitude: ").place(x=0, y=225)

upid.place(x=75, y=25, width=300)
upstart = ttk.Entry(upframe)
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
"""

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
{
            "itemID": 10867,
            "inheritToAllChildren": "false",
            "inheritToChildren" : [],
            "event": {
                "startDate": 1,
                "endDate": 1,
                "label": "Test",
                "description": "Testdesc",
                "eventType":  53,
                "latitude": 0,
                "longitude": 0,
                "elevationInMeter": 0,
                "id": None
            }




"""
login()
root.mainloop()
