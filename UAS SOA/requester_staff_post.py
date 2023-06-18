# library untuk JSON
import json
# library untuk transfer data
import requests


# ambil data dari database, atau dari data internal di program
data = {'namaStaff'   : 'mika2', 
        'userStaff' : 'mika2', 
        'passwordStaff' : 'mika2',
        'noTelpStaff' : '088465468688',
        'alamatStaff' : 'Jl Kalimantan 1'
        }

# ubah data ke JSON
jsondoc = json.dumps(data)

# kirim post request ke server
response = requests.post('http://localhost:5000/eo/staff/register', data=jsondoc)
if (response.status_code == 200):
    print('DATA BERHASIL DITAMBAHKAN')
else:
    print('Error Code: ' + str(response.status_code))

