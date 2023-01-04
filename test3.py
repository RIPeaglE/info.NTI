import requests
import json

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

resp = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers,verify=False)
#print(response.text)


for t in resp.json():
    params = {
        'mot': t['destination'],
        'linje': t['transport']['line'],
        'om': t['time']['displayTime'],
        'stop': t['track']
    }
    #print(params)


try: 
    for s in resp.json():
        p = ( s['transport']['line'] + " mot " + s['destination'] + " om: " + s['time']['displayTime'] + " från stop: " + s['track'])
        print(p)
        
except:
    print("error")