import datetime
import json
import logging
import tkinter as tk
from tkinter import ttk
from geopy.geocoders import Nominatim
import requests

geolocation = Nominatim(user_agent="SENSOR-Event-Manger")


class App:
    def __init__(self):
        # defining the root window
        self.root = tk.Tk()
        self.root.title("Event Writer")
        self.root.geometry("1280x720")
        self.root.config(bg="#07ace7")
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def locationTop(self):
        # build window on top of main
        self.loca = tk.Toplevel()
        self.loc = ttk.Frame(self.loca)
        self.loc.pack()
        ttk.Label(self.loc, text="Search location by name").grid(column=0, row=0, columnspan=3)
        ttk.Label(self.loc, text="Enter Location Name:").grid(column=0, row=1)
        self.locinfo = tk.Text(self.loc, width=50, height=10)
        self.locinfo.grid(column=0, row=3, columnspan=3)
        self.geosearch = ttk.Entry(self.loc, width=30)
        self.geosearch.grid(column=1, row=1)
        self.search_button = ttk.Button(self.loc, command=self.getLocation, text="Get Location")
        self.search_button.grid(column=0, row=4, columnspan=2)
        self.geosearch.bind("<Return>", self.getLocation)
        self.search_button.bind("<Return>", self.getLocation)

    def getLocation(self, a=None):
        try:
            location = geolocation.geocode(self.geosearch.get())
            print(location.address)
            self.inlongintude.delete(0, "end")
            self.inlatitude.delete(0, "end")
            self.inelevation.delete(0, "end")
            self.locinfo.delete('1.0', "end")
            self.inlongintude.insert(0, location.longitude)
            self.inlatitude.insert(0, location.latitude)
            self.inelevation.insert(0, location.altitude)
            self.locinfo.insert('1.0', location.address)
        except Exception as ex:
            print(ex)
            self.locinfo.delete("1.0", "end")
            self.locinfo.insert("1.0", "Error: Timeout / Location can not be found")

    def geteventtype(self, a=None):
        self.eventtypefromdd = int(''.join(list(filter(str.isdigit, self.clicked.get()))))

    def searchbyid(self, a=None):
        """this function searches for a sensor by its id"""
        try:
            self.sid = self.senid.get()
            url = f'https://sandbox.sensor.awi.de/rest/sensors/device/getDevice/{self.sid}'
            self.sensor = requests.get(url)
            self.sensor = self.sensor.json()
            self.setMeta(self.sensor)
            self.getupdate()
        except ValueError:
            x = "Input outside of search zone"
            self.errorwin(x)

    def setMeta(self, a):
        """this function sets the meta information in the sensor information frame to the current sensor used"""

        self.isenid.config(state=tk.NORMAL)
        self.iurn.config(state=tk.NORMAL)
        self.ishortname.config(state=tk.NORMAL)
        self.ilongname.config(state=tk.NORMAL)
        self.isenid.delete(0, "end")
        self.iurn.delete(0, "end")
        self.ishortname.delete(0, "end")
        self.ilongname.delete(0, "end")
        self.isenid.insert(0, a['id'])
        self.iurn.insert(0, a['urn'])
        self.ishortname.insert(0, a["shortName"])
        self.ilongname.insert(0, a["longName"])
        self.isenid.config(state=tk.DISABLED)
        self.iurn.config(state=tk.DISABLED)
        self.ishortname.config(state=tk.DISABLED)
        self.ilongname.config(state=tk.DISABLED)

    def selectItem(self):
        """"this functions returns the id of the sensor selected in the treeview menu"""
        i = self.tw.focus()
        h = self.tw.item(i)

        if h["values"] == "":
            pass
        else:
            self.senid.delete(0, "end")
            self.senid.insert(0, h["values"])
            if self.tw.get_children(i):
                pass
            else:
                childs = requests.get(
                    f"https://sandbox.sensor.awi.de/rest/sensors/device/getChildrenOfDevice/{self.senid.get()}")
                childs = childs.json()
                for iiix, child in enumerate(childs):
                    self.tw.insert(i, index=iiix, text=child["shortName"], values=child["id"])  #
                    print(child["shortName"])
            self.searchbyid()
    def getdate(self):
        self.ti = str(datetime.datetime.utcnow())
        self.ti = self.ti[0:10] + "T" + self.ti[11:19]
        self.instart.insert(0, self.ti)
        self.inend.insert(0, self.ti)
    def login(self):
        """login code by maximilian betz; used to login on sensor api service"""
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
                self.errorwin("Login to SENSOR.awi.de failed.")
                raise Exception('Could not login. {} Status code: {}'.format(response.text, response.status_code))
            else:
                print("Login Successful")
            self.token = response.cookies['x-auth-token']

        except Exception as e:
            logging.error("Communication error to sensor.awi.de: {}".format(e))

    def getupdate(self):
        # get current data from entry boxes and save in dictonary
        self.eventdata["deviceid"] = self.isenid.get()
        self.eventdata["description"] = self.indescription.get(1.0, "end")
        self.eventdata["longitude"] = self.inlongintude.get()
        self.eventdata["latitude"] = self.inlatitude.get()
        self.eventdata["altitude"] = self.inelevation.get()
        self.eventdata["label"] = self.inlabel.get()
        self.eventdata["deviceid"] = self.senid.get()
        self.eventdata["startdate"] = self.instart.get()
        self.eventdata["enddate"] = self.inend.get()
        try:
            self.eventdata["eventtype"] = str(self.eventtypefromdd)
        except:
            pass
        print(self.eventdata)

    def errorwin(self, error):
        """function for creating error message boxes"""
        self.errwin = tk.Toplevel()
        self.errwin.resizable(False, False)
        self.errwin.geometry("1260x200")
        self.err = ttk.Frame(self.errwin)
        self.err.place(x=0, y=0, width=4000, height=2000)
        ttk.Label(self.errwin, text="Error:", font="Calibri 20").pack()
        ttk.Label(self.errwin, text=error, font="Calibri 12").pack()
        okbutton = ttk.Button(self.errwin, text="OK", command=self.errwin.destroy)
        okbutton.pack()
        okbutton.focus_set()
        def quit(a=None):
            self.errwin.destroy()
        self.errwin.bind("<Return>", quit)

    def upload(self):
        """Here the data gets actually uploaded via api"""
        uploaddata = {
            "itemID": self.eventdata['deviceid'],
            "inheritToAllChildren": True,
            "inheritToChildren": [
                0
            ],
            "event": {
                "startDate": f"{self.eventdata['startdate']}",
                "endDate": f"{self.eventdata['enddate']}",
                "label": f"{self.eventdata['label']}",
                "description": f"{self.eventdata['description']}",
                "eventType": self.eventdata["eventtype"],
                "longitude": self.eventdata['longitude'],
                "latitude": self.eventdata['latitude'],
                "elevationInMeter": self.eventdata["altitude"],
                "id": None
            }
        }
        headers = {"Content-Type": "application/json"}
        url = f"https://sandbox.sensor.awi.de/rest/sensors/events/putEvent/{self.eventdata['deviceid']}?createVersion=false"
        response = requests.put(url, data=json.dumps(uploaddata), headers=headers, cookies={'x-auth-token': self.token})
        print(self.token)
        print(url)
        print(headers)
        print(json.dumps(uploaddata))
        print(response)
        if response.status_code != 201:
            self.errorwin("Transfer to SENSOR.awi.de FAILED!")
            raise Exception("Transfer to SENSOR.awi.de FAILED!")
        else:
            self.cwin.destroy()
            fine = tk.Toplevel(self.root)
            fine.title("Upload Successful")
            fine.geometry("500x100")
            fine_frame = ttk.Frame(fine)
            fine_frame.place(x=0, y=0, width=500, height=500)
            ttk.Label(fine_frame, text="Upload Successful!", font=("Calibri", 30)).pack()
            ttk.Button(fine_frame, text="Ok", command=fine.destroy).pack()

    def confirm(self):
        """Function to open a confirm window on upload begin"""
        if self.inlabel.get() == '':
            self.errorwin("You need to assign a label to be able to upload!")
            return
        self.getupdate()
        self.cwin = tk.Toplevel(self.root)
        self.cwin.geometry("700x500")
        cframe = ttk.Frame(self.cwin)
        cframe.place(x=0, y=0, width=1000, height=1000)
        ttk.Label(cframe, text="You are about to upload following action to SENSOR.awi.de").place(x=0, y=0)
        ttk.Label(cframe, text=f"DeviceID: {self.eventdata['deviceid']}").place(x=0, y=30)
        ttk.Label(cframe, text=f"Label: {self.eventdata['label']}").place(x=0, y=60)
        ttk.Label(cframe, text=f"Start Date: {self.eventdata['startdate']}").place(x=0, y=90)
        ttk.Label(cframe, text=f"End Date: {self.eventdata['enddate']}").place(x=0, y=120)
        ttk.Label(cframe, text=f"Event Type: {self.eventdata['eventtype']}").place(x=0, y=150)
        ttk.Label(cframe, text=f"Longitude: {self.eventdata['longitude']}").place(x=0, y=180)
        ttk.Label(cframe, text=f"Latitude: {self.eventdata['latitude']}").place(x=0, y=210)
        ttk.Label(cframe, text=f"Altitude: {self.eventdata['altitude']}").place(x=0, y=240)
        ttk.Label(cframe, text=f"Description: {self.eventdata['description']}").place(x=0, y=270)
        ttk.Label(cframe,
                  text="Please be aware that this action can't be undone by this program and need to be undone through the web interface.").place(
            x=0, y=430)

        ttk.Button(cframe, text="Im sure, go upload", command=self.upload).place(x=300, y=450)
        ttk.Button(cframe, text="STOP", command=self.cwin.destroy).place(x=200, y=450)

    def sensorframe(self):
        # information and selection of sensor
        self.senframe = ttk.Frame(self.root)
        self.senframe.place(x=0, y=0, height=360, width=640)

        ttk.Label(self.senframe, text="Sensor Event Manager").place(x=0, y=0)

        self.tw = ttk.Treeview(self.senframe)
        self.tw.place(x=0, y=25, width=200, height=330)

        # scrollbar for treeview
        self.twsb = ttk.Scrollbar(self.senframe, orient="vertical", command=self.tw.yview, cursor="double_arrow")
        self.twsb.place(x=200, y=25, width=20, height=330, anchor="ne")

        self.searchidbutton = ttk.Button(self.senframe, command=self.searchbyid, width=20, text="Search by ID")
        self.searchidbutton.place(x=500, y=0, width=130)

        self.senid = ttk.Entry(self.senframe, width=40)
        self.senid.place(x=200, y=0, width=300)
        self.senid.bind("<Return>", func=self.searchbyid)

        # meta information about selected sensor
        ttk.Label(self.senframe, text="Data of selcted sensor").place(x=200, y=25)
        ttk.Label(self.senframe, text="SensorID:").place(x=210, y=45)
        ttk.Label(self.senframe, text="URN:").place(x=210, y=70)
        ttk.Label(self.senframe, text="Shortname:").place(x=210, y=95)
        ttk.Label(self.senframe, text="Longname:").place(x=210, y=120)

        self.isenid = ttk.Entry(self.senframe)
        self.isenid.place(x=300, y=45, width=300)
        self.iurn = ttk.Entry(self.senframe)
        self.iurn.place(x=300, y=70, width=300)
        self.ishortname = ttk.Entry(self.senframe)
        self.ishortname.place(x=300, y=95, width=300)
        self.ilongname = ttk.Entry(self.senframe)
        self.ilongname.place(x=300, y=120, width=300)

        # make it possible to select items in treeview menu
        self.tw.bind('<ButtonRelease-1>', self.selectItem)

    def eventframe(self):
        # event input frame
        self.evframe = ttk.Frame(self.root)
        self.evframe.place(x=640, y=0, height=720, width=640)
        ttk.Style.configure(self.style, "l.Label", font=(None, 20))
        ttk.Label(self.evframe, text="Enter event data below", style="l.Label").place(x=0, y=0)

        # dropdown for possible events from api
        self.clicked = tk.StringVar()
        self.possibevents = ['Select Event']
        self.dd = ttk.OptionMenu(self.evframe, self.clicked, *self.possibevents, command=self.geteventtype)
        self.dd.place(x=80, y=50, width=400)


        # input entry box description
        ttk.Label(self.evframe, text="Label:").place(x=0, y=85)
        ttk.Label(self.evframe, text="Description:").place(x=0, y=300)
        ttk.Label(self.evframe, text="Longitude:").place(x=0, y=160)
        ttk.Label(self.evframe, text="Latitude:").place(x=250, y=160)
        ttk.Label(self.evframe, text="Altitude:").place(x=0, y=185)
        ttk.Label(self.evframe, text="Start Time:").place(x=0, y=110)
        ttk.Label(self.evframe, text="End Time:").place(x=250, y=110)
        ttk.Label(self.evframe, text="Attention: Format sensetive | UTC timezone").place(x=80, y=135)

        # event input boxes
        self.inlabel = ttk.Entry(self.evframe)
        self.inlabel.place(x=80, y=85, width=400)

        self.inlongintude = ttk.Entry(self.evframe)
        self.inlongintude.place(x=80, y=160)

        self.inlatitude = ttk.Entry(self.evframe)
        self.inlatitude.place(x=350, y=160)

        self.inelevation = ttk.Entry(self.evframe)
        self.inelevation.place(x=80, y=185)

        self.instart = ttk.Entry(self.evframe)
        self.instart.place(x=80, y=110)

        self.inend = ttk.Entry(self.evframe)
        self.inend.place(x=350, y=110)

        self.indescription = tk.Text(self.evframe, font=("Calibri 10"))
        self.indescription.place(x=80, y=300, width=400, height=300)

        ttk.Button(self.evframe, text="Get location by name search", command=self.locationTop).place(x=80, y=210, width=400)

    def uploadframe(self):
        # frame bottom left, simply holds upload button in place
        self.upframe = ttk.Frame(self.root)
        self.upframe.place(x=0, y=360, width=640, height=360)
        ttk.Button(self.upframe, text="Upload to SENSOR", command=self.confirm, style="b.TButton").place(x=30, y=30,
                                                                                                    width=500,
                                                                                                    height=250)
        ttk.Style.configure(self.style, "b.TButton", font=(None, 30))

    def settree(self):

        # get all collections through api
        collections = requests.get("https://sandbox.sensor.awi.de/rest/sensors/collections/getAllCollections")
        collections = collections.json()

        # add collections to treeview
        for ix, col in enumerate(collections):
            print(ix)
            print(col["collectionName"])
            # get sensors from api
            items = requests.get(
                f"https://sandbox.sensor.awi.de/rest/sensors/collections/getItemsOfCollection/{col['id']}")
            items = items.json()
            main = self.tw.insert('', index=ix, text=col["collectionName"])
            # set child sensor of item
            for iix, item in enumerate(items):
                self.childinsert = self.tw.insert(main, index=iix, text=item["shortName"], values=item["id"])

    def setevent(self):
        # get all possible events from api
        events = requests.get("https://sandbox.sensor.awi.de/rest/sensors/events/getAllEventTypes")
        events = events.json()
        self.clicked.set("Select Event")
        for ix, ev in enumerate(events):
            print(ix)
            print(ev["generalName"])
            self.possibevents.append(ev["generalName"] + " (" + str(ev["id"]) + ")")
        self.dd.set_menu(*self.possibevents)
    def initvars(self):
        # event data dictionary that holds data until upload
        self.eventdata = {
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

    def startprogram(self):
        self.initvars()
        self.settree()
        self.setevent()
        self.login()
        self.getdate()

    def run(self):
        self.sensorframe()
        self.eventframe()
        self.uploadframe()
        self.root.after(100, self.startprogram)
        self.root.mainloop()




program = App()
program.run()