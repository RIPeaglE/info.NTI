import requests
import json
import datetime

from datetime import datetime

# get current datetime
dt = datetime.now()

# get day of week as an integer
x = dt.weekday()
x = x + 1

# Get the data from the Gettime's database 'https://gettime.ga/API/JSON
params = {
    'school': '0',
    'id': '20EL2',
    'day': x,
}

response = requests.get('https://gettime.ga/API/JSON', params=params)
data = json.loads(response.text)
for lesson in data["data"]["data"]["lessonInfo"]:
    print(lesson)
