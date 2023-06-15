# library untuk JSON
import json
# library untuk transfer data
import requests


# ambil data dari database, atau dari data internal di program
# data = {'nama'   : 'Yoshinoya',
#         'gedung' : 'Gedung Q',
#         'produk' : [{'menu':'Yakiniku', 'price': '65000'},
#                     {'menu':'Egg mayo', 'price': '35000'}] }
# data = {'nama'   : 'Excelso',
#         'gedung' : 'Gedung Q',
#         'produk' : [{'menu':'Cappucino', 'price': '47000'},
#                     {'menu':'Espresso', 'price': '29000'}] }

data = {"id_client": 1,
        "order_name": "dummyOrder1",
        "order_description": "dummydesk",
        "order_date": "2023-06-15",
        "total_price": 100,
        "status": "Processing"}

jsondoc = json.dumps(data)
response = requests.post('http://localhost:5000/order', data=jsondoc)
if (response.status_code == 201):
    data = response.json()
    print('DATA BERHASIL DITAMBAHKAN')
    print('Kode baru: ' + str(data['id']))
else:
    print('Error Code: ' + str(response.status_code))


