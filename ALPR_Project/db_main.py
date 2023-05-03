import subprocess
import random
import mysql.connector
import json

number_plate = ""
status = True

with open('plate_info.json', 'w') as file:
    random_nr = random.randint(1000000, 999999999)
    pic = subprocess.run(f'fswebcam -r 3840x2160 {random_nr}.jpg', shell=True)
    # info = subprocess.run(f'alpr -c eu -j -n 1 {random_nr}.jpg', shell=True, stdout=file)
    info = subprocess.run(f'alpr -c eu -j -n 1 {random_nr}.jpg', shell=True, stdout=file)

with open('plate_info.json', 'r') as file:
    json_file = json.load(file)

    for i in json_file['results']:
        number_plate = i['plate']


print('[*] Connecting to server...')

db = mysql.connector.connect(
    host='38.242.159.2',
    user='jjg',
    passwd='JJGadmin174!',
    database='plates'
)   

mycursor = db.cursor()

print('[+] Connection established.')
mycursor.execute(f"SELECT * FROM numbers")
for name, plate in mycursor:
    if plate == number_plate:
        print(f'[+] Plate recognised. Plate: {plate}, Owner: {name}')
        print('[+] Rising slagbaumas')
        print('[*] Closing connection with database')
        status = False
        break
    else:
        pass
if status == True:
    print('[-] No plate was identified.')
    print('[*] Closing connection with database.')


db.close()
