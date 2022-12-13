import requests
import json
import datetime
from flask import Flask
from flask import render_template
import feedparser
from flask import Markup
from bs4 import BeautifulSoup


from datetime import datetime

#klasser = ['20el1','20el2','20teks','20teks','20teke','20de','21el','21tek','21de','22tek','22el','22de','22yrkel']
klasser = []
# get current datetime
dt = datetime.now()
now = datetime.now()

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
things = []
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
        denna_timme = int(dt.now().strftime("%H"))
        try:
            for x in data['data']['data']['lessonInfo']: 
                temp = f"{x['timeStart']} -- {x['texts'][0]}: Börjar kl {x['timeStart']} och slutar kl {x['timeEnd']}"
                try:
                    temp += f" i sal {x['texts'][2]}"
                except:
                    pass
                #Gets the lesson times for the current hour
                if denna_timme >= int(x['timeStart'].split(':')[0]) and denna_timme <= int(x['timeEnd'].split(':')[0]):
                    temp = "Pågående lektion: " + temp
                    a.append(temp)
            a.sort()

            a = [i.split(' -- ')[1] for i in a]
            a.append(klass)
            

            things.append(a)

            
            print(klass)
            for x in a:
                print('\n' + x)
            print("--------------")
        except TypeError:
            print("No class found with such name")
    return things
         
Lektiontider = time()

#Skolmaten
#https://skolmaten.se/nti-gymnasiet-sodertorn/
#https://skolmaten.se/about/rss/nti-gymnasiet-sodertorn/
NewsFeed = feedparser.parse("https://skolmaten.se/nti-gymnasiet-sodertorn/rss/days/")

print('Number of RSS posts :', len(NewsFeed.entries))

entry = NewsFeed.entries[0]
#print('Post Title :',entry.title)
print('Post Summary :',entry.summary)

skolmaten = Markup(entry.summary)

#Weathers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 
 
def weather():
    Huddinge = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={Huddinge}&oq={Huddinge}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location + " " + weather+"°C")
    print(info)
    return location + " " + weather+"°C" + ": " + info

city = 'Huddinge'
city = city+" weather"
weather = weather()

#Week
week_number_new = dt.isocalendar().week
print ("Vecka: " + str(week_number_new))
week = week_number_new

#Flask
app = Flask(__name__)
 
@app.route('/')
def home():
        return render_template('front.html', Lektiontider=Lektiontider, skolmaten=skolmaten, weather=weather, week=week)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
