# library untuk JSON
import json
# library untuk transfer data
import requests


data = {"id_order": 4,
        "id_staffPIC": 1,
        "event_name": "dummyEventPUT",
        "event_description": "deskDummy1",
        "event_date": "2023-07-15",
        "start_time": "02:00:00",
        "end_time": "02:30:00",
        "sub_total": 250
        }

jsondoc = json.dumps(data)
response = requests.put('http://localhost:5001/event/6', data=jsondoc)
if (response.status_code == 200):
    data = response.json()
    print('DATA BERHASIL DIEDIT')
    print('Kode baru: ' + str(data['id']))
else:
    print('Error Code: ' + str(response.status_code))

