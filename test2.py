import requests
import json

headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv,en-US;q=0.9,en;q=0.8',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89RmxlbWluZ3NiZXJncyBzdGF0aW9uIChIdWRkaW5nZSlAWD0xNzk0Nzk4OEBZPTU5MjE5MjM2QFU9NzRATD0zMDAxMDcwMDZAQj0xQHA9MTY3MzQ5MjQyMEA=',
    'origSiteId': '7006',
    'desiredResults': '3',
    'origName': 'Flemingsbergs station (Huddinge)',
}

response = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers, verify=False)
#print(response.text)

SLpendel = []
for o in response.json():
    params = {
        'linje': o['transport']['line'],
        'mot': o['destination'],
        'om': o['time']['displayTime'],
        'transportType': o['transport']['transportType'],
        'stop': o['track']
    }
    for key, value in params.items():
        if key == "transportType" and value == "Train":
            z = f"Linje {params['linje']} mot {params['mot']} om: {params['om']} från STOP: {params['stop']}"
            print(z)
            SLpendel.append(z)
