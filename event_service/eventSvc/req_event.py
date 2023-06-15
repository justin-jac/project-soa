# library untuk JSON
import json
# library untuk transfer data
import requests

data = {"id_order": 4,
        "id_staffPIC": 1,
        "event_name": "dummyEvent1",
        "event_description": "deskDummy1",
        "event_date": "2023-06-15",
        "start_time": "01:00:00",
        "end_time": "01:30:00",
        "sub_total": 200
        }

jsondoc = json.dumps(data)
response = requests.post('http://localhost:5001/event', data=jsondoc)
if (response.status_code == 201):
    data = response.json()
    print('DATA BERHASIL DITAMBAHKAN')
    print('Kode baru: ' + str(data['id']))
else:
    print('Error Code: ' + str(response.status_code))


