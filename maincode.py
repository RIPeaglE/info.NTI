import requests
import json
import datetime
from flask import Flask
from flask import render_template
import feedparser
from flask import Markup
from bs4 import BeautifulSoup
import locale



from datetime import datetime

#klasser = ['20el1','20el2','20teks','20teks','20teke','20de','21el','21tek','21de','22tek','22el','22de','22yrkel']
klasser = []
# get current datetime

dt = datetime.now()
#now = datetime.now()

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
        timplus = str(dt.now().strftime("%H")) + str(dt.now().strftime("%M"))
        dennatimme = int(timplus)
        try:
            for x in data['data']['data']['lessonInfo']: 
                temp = f"{x['timeStart']} -- {x['texts'][0]}: Börjar kl {x['timeStart']} och slutar kl {x['timeEnd']}"
                try:
                    temp += f" i sal {x['texts'][2]}"
                except:
                    pass
                #Gets the lesson times for the current hour
                startplus = str(x['timeStart'].split(':')[0]) + str(x['timeStart'].split(':')[1])
                endplus = str(x['timeEnd'].split(':')[0]) + str(x['timeEnd'].split(':')[1])
                start = int(startplus)
                end = int(endplus)
                if dennatimme >= start and dennatimme <= end:
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
#############

#Skolmaten
#https://skolmaten.se/nti-gymnasiet-sodertorn/
#https://skolmaten.se/about/rss/nti-gymnasiet-sodertorn/
NewsFeed = feedparser.parse("https://skolmaten.se/nti-gymnasiet-sodertorn/rss/days/")

print('Number of RSS posts :', len(NewsFeed.entries))

entry = NewsFeed.entries[0]
#print('Post Title :',entry.title)
print('Post Summary :',entry.summary)

skolmaten = Markup(entry.summary)
#############

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
#############

#Week
week_number_new = dt.isocalendar().week
print ("Vecka: " + str(week_number_new))
week = week_number_new
#############

#Gets current date in format: Monday, 1 January. But its not working because i already use datetime. Have to find a way to fix it.
#ddm = datetime.datetime.now()
locale.setlocale(locale.LC_TIME, "sv_SE") # swedish
print(dt.strftime("%A, %d %B"))
date = dt.strftime("%A, %d %B")

#############

#SL
headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89SHVkZGluZ2Ugc2p1a2h1cyAoSHVkZGluZ2UpQFg9MTc5Mzc1NDNAWT01OTIyMjI2NUBVPTc0QEw9MzAwMTA3MDAwQEI9MUBwPTE2NzA5ODY4MTBA',
    'origSiteId': '7000',
    'desiredResults': '10',
    'origName': 'Huddinge sjukhus (Huddinge)',
}

response = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers,verify=False)
print(response.text)

#(destination)(line)(displayTime)(track)
#############


#Flask
app = Flask(__name__)
 
@app.route('/')
def home():
        return render_template('front.html', Lektiontider=Lektiontider, skolmaten=skolmaten, week=week, datum=date, SLbuss=response.text, weather=weather)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
