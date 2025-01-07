import json
import requests

card_parameter = input('Param: ') # takes in parameter for search
corresponding_variable = input('Variable: ') # the variable correspoding to the parameter that the user wants to actually search for like a specific card type or card.



r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={ # send request into ygoprodeck api
    f'{card_parameter}' : f'{corresponding_variable}',})


def jprint(obj): # function that allows the printing of the data retruend by the api
    text = json.dumps(obj, sort_keys= True, indent= 4)
    print(text)


if r.status_code == 200: # checks if connection between api and code works
    jprint(r.json())
else:
    print('error')
