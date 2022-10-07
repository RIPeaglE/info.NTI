import requests
import json
import datetime

from datetime import datetime
# get current datetime
dt = datetime.now()

# get day of week as an integer
x = dt.weekday()
x = x + 1

#Json code from https://www.geeksforgeeks.org/json-load-in-python/
f = open('klasser.json',)
   
# returns JSON object as 
# a dictionary
data = json.load(f)
   
# Iterating through the json
# list
for i in data['overwriteOtherData']['data']['classes']:
    print(i)
   
# Closing file
f.close()


params = {
'school': '0',
'id': i,
'day': x,
}

    # Gets the data from the Gettime's database 'https://gettime.ga/API/JSON'


response = requests.get('https://gettime.ga/API/JSON', params=params)
data = json.loads(response.text)

a = []

try:
    for x in data['data']['data']['lessonInfo']:
        temp = f"{x['timeStart']} -- {x['texts'][0]}, börjar kl {x['timeStart']} och slutar kl {x['timeEnd']}"
        try:
            temp += f" i sal {x['texts'][2]}"
        except:
            pass
        a.append(temp)
    a.sort()

    a = [i.split(' -- ')[1] for i in a]

    for x in a:
        print(x+'\n')
except TypeError:
    print("No class found with such name")


