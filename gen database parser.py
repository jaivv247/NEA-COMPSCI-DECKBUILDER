import json
import requests

# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH

list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale,cardset','archetype','banlist','format','misc','has_effect'] #LIST OF ACCEPTABLE PARAMETERS
list_of_types = ["effect Monster","flip effect monster","flip tuner effect monster","gemini Monster","Normal Monster","Normal Tuner Monster","Pendulum Effect Monster","Pendulum Effect Ritual Monster","Pendulum Flip Effect Monster","Pendulum Normal Monster","Pendulum Tuner Effect Monster","Ritual Effect Monster","Ritual Monster","Spell Card","Spirit Monster","Toon Monster","Trap Card","Tuner Monster","Union Effect Monster"
,"Fusion Monster","Link Monster","Pendulum Effect Fusion Monster","Synchro Monster","Synchro Pendulum Effect Monster","Synchro Tuner Monster","XYZ Monster","XYZ Pendulum Effect Monster","Skill Card","Token"]


card_valid = False
while card_valid == False:
    card_parameter = input('what ygo api type thing are you searching for: ') # THIS LINE TAKES A PARAMETER
    corresponding_variable = input('corresponding: ')

    match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
        case 'id':
            if corresponding_variable.digit() = True:
                #card_valid = True
            else:
                print('id is incorrect format please try again')
        case 'type':
            if corresponding_variable in list_of_types:



r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
    f'{card_parameter}' : f'{corresponding_variable}',})


def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent= 4)
    print(text)


if r.status_code == 200:
    jprint(r.json())





else:
    print('error')