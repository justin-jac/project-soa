# library untuk JSON
import json
# library untuk transfer data
import requests


data = {"id_client": 1,
        "order_name": "dummyOrderdummyput",
        "order_description": "dummydesk",
        "order_date": "2023-06-15",
        "total_price": 100,
        "status": "Completed"}

jsondoc = json.dumps(data)
response = requests.put('http://localhost:5000/order/3', data=jsondoc)
if (response.status_code == 200):
    data = response.json()
    print('DATA BERHASIL DIEDIT')
    print('Kode baru: ' + str(data['id']))
else:
    print('Error Code: ' + str(response.status_code))

