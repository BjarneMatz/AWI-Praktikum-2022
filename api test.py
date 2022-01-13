import json
import requests

eventdata = {
  "itemID": 10867,
  "inheritToAllChildren": True,
  "inheritToChildren": [
    0
  ],
  "event": {
    "startDate": "2020-01-01T14:10:00",
    "endDate": "2020-01-01T14:10:00",
    "label": "Test",
    "description": "string",
    "eventType": 15,
    "longitude": 21,
    "latitude": 8,
    "elevationInMeter": 55,
    "id": None
  }
}

with open('accounts.json', encoding='utf-8') as f:
    accounts = json.load(f)

try:
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
    print(response.status_code)
    print("Token: " + token)
except Exception as ex:
    print(ex)

headers = {"Content-Type": "application/json"}
url = "https://sandbox.sensor.awi.de/rest/sensors/events/putEvent/10867"
response = requests.put(url, data=json.dumps(eventdata), headers=headers, cookies={'x-auth-token': token})
print("RAW Python Data: " + str(eventdata))
print("JSON Dump: " + json.dumps(eventdata))
print(response)
print(response.status_code)
