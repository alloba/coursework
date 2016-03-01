'''
Hyun Oh
Software Engineering Group Project
Updating League of Legend champion information and adding it to a file called "champ_info.txt"
'''
import requests
import json

#user info and login info
api_key = 'cd055e34-b362-4ea6-8c4b-3b1086d17c92'
api_call = "https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion/?api_key=" + api_key


#get champion info
param = {'champData': 'all'}
r = requests.get(api_call, param, timeout=5)

#decode json data
champ_info = r.json()

#check status
print("status", r.status_code)
print("raise-for-status", r.raise_for_status())
for h in r.headers:
    print(h, r.headers[h])

#print champ info keys
print("key", champ_info.keys())
print("data key:",champ_info['data'].keys())
print("fiora key:", champ_info['data']['Fiora'].keys())
print("passive:", champ_info['data']['Fiora']['passive'].keys())

#write to text file
json.dump(champ_info, open("champ_info.txt",'w'))


