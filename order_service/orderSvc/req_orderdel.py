# library untuk JSON
import json
# library untuk transfer data
import requests

# jsondoc = json.dumps(data)
response = requests.delete('http://localhost:5000/order/3')
if (response.status_code == 200):
    data = response.json()
    print('DATA BERHASIL DIdelete')
    print('Kode baru: ' + str(data['id']))
else:
    print('Error Code: ' + str(response.status_code))

