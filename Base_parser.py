import json
import requests

card_parameter = input('Param: ')
corresponding_variable = input('Variable: ')



r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
    f'{card_parameter}' : f'{corresponding_variable}',})


def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent= 4)
    print(text)


if r.status_code == 200:
    jprint(r.json())
else:
    print('error')
