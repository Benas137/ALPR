import json
import subprocess
import random


while True:
    with open('plate_info.json', 'w') as file:
        random_nr = random.randint(1000000, 999999999)
        pic = subprocess.run(f'fswebcam -r 3840x2160 {random_nr}.jpg', shell=True)
        info = subprocess.run(f'alpr -c eu -j -n 1 {random_nr}.jpg', shell=True, stdout=file)

    status = True
    number_plate = ""
    number_plates = {}

    with open('plate_info.json', 'r') as file, open('mokytoju_numeriai.json', 'r') as plate_file:
        json_mokytoju = json.load(plate_file)
        json_file = json.load(file)

        for i in json_file['results']:
            number_plate = i['plate']

        for i, name in json_mokytoju['numeriai'].items():
            number_plates[i] = name

        for plate, name in number_plates.items():
            if number_plate == plate:
                print('[+] Number plate detected. Plate: {}, Owner {}'.format(number_plate, name))
                status = False
                break
        if status == True:
            print('[-] Number is not valid or not detected')
    break


