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
f = open("klasser.json", "r")
x = f.read()
d = json.loads(x)

snart = d['overwriteOtherData']['data']['classes']
klasser = []

for klass in snart:
    namn = klass['groupName']
    klasser.append(namn)

#print(klasser)



a = []

try:
    for x in d['data']['data']['lessonInfo']:
        temp = f"{x['timestart']} -- {x['texts'][0]}, börjar kl {x['timestart']} och slutar kl {x['timeend']}"
        try:
            temp += f" i sal {x['texts'][2]}"
        except:
            pass
        a.append(temp)
    a.sort()

    a = [i.split(' -- ')[1] for i in a]

    for x in a: 
        print (x+'\n')
except TypeError:
    print ("No class found with such name")