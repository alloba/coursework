from riotwatcher import RiotWatcher
import json
import urllib.request, urllib.error
import os


datadragon_json_path = 'http://ddragon.leagueoflegends.com/cdn/6.3.1/data/en_US/champion.json'
datadragon_json_local_path = 'champion.json'
champion_image_directory = os.curdir + "/Champion_Images/"

try:
    response = urllib.request.urlopen(datadragon_json_path).read().decode('utf-8')
    rawjson = json.loads(response)
except (urllib.error.URLError, urllib.error.HTTPError) as e:
    rawjson = json.loads(open(datadragon_json_local_path,'r').read())


champ_dictionary = rawjson['data']
champion_name_list = champ_dictionary.keys()


def get_champ_id(champ_name):
    return champ_dictionary[champ_name]['id']


def downloadimage(champ_name):
    champion_image_url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+champ_name+'_0.jpg'

    if not os.path.exists(champion_image_directory):
        os.makedirs(champion_image_directory)

    image_response = urllib.request.urlopen(champion_image_url).read()

    imagefile = open(champion_image_directory + champ_name + '.jpg', 'wb')
    imagefile.write(image_response)


def get_element(champ_name, element_name):
    if champ_name in champ_dictionary:
        try:
            return champ_dictionary[champ_name][element_name]
        except KeyError:
            return "Unrecognized Element Name"
    else:
        return "Unrecognized Champion Name"


def get_champ_stats(champ_name, stat_name):
    if champ_name in champ_dictionary:
        try:
            return champ_dictionary[champ_name]['stats'][stat_name]
        except KeyError:
            return "Unrecognized Stat Name"
    else:
        return "Unrecognized Champion Name"


print(get_element('Zyra', 'blurb'))
print(get_champ_stats('Zyra', 'hp'))
#w = RiotWatcher('be90127a-78ef-4dcf-a985-3bd5bca51235')
