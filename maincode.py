import requests
import json
import datetime

from datetime import datetime

#klasser = ['20el1','20el2','20teks','20teks','20teke','20de','21el','21tek','21de','22tek','22el','22de','22yrkel']
klasser = []
# get current datetime
dt = datetime.now()

# get day of week as an integer
day = dt.weekday() + 1

#Json code from https://www.geeksforgeeks.org/json-load-in-python/
f = open('klasser.json', "r")
   
# returns JSON object as 
# a dictionary
data = json.load(f)
   
# Iterating through the json
# list
for i in data['overwriteOtherData']['data']['classes']:
    klasser.append(i['groupName'])
   
# Closing file
f.close()

#I put the code insde a function so I can use it later for with flask
def time():
    for klass in klasser:
        params = {
        'school': '0',
        'id': klass,
        'day': day,
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
            print("-------------------------------------------------------------------------------------------")
            print(klass)
            for x in a:
                print('\n' + x)
            print("-------------------------------------------------------------------------------------------")
        except TypeError:
            print("No class found with such name")
time()

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('frontend.html'), time()

if __name__ == '__main__':
    app.run(debug=True)