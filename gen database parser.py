import json
import requests

# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH

list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale,cardset','archetype','banlist','format','misc','has_effect'] #LIST OF ACCEPTABLE PARAMETERS
list_of_types = ["effect Monster","flip effect monster","flip tuner effect monster","gemini monster","normal monster","normal tuner monster","pendulum effect monster","pendulum effect ritual monster","pendulum flip effect monster","pendulum normal monster","pendulum tuner effect monster","ritual effect monster","ritual monster","spell card","spirit monster","toon monster","trap card","tuner monster","union effect monster"
,"fusion monster","link monster","pendulum effect fusion monster","synchro monster","synchro pendulum effect monster","synchro tuner monster","xyz Monster","xyz pendulum effect monster","skill card","token"]

cardparam_valid = False
cardvariable_valid = False
while card_valid == False and cardparam_valid == False:
card_parameter = input('what ygo api type thing are you searching for: ') # THIS LINE TAKES A PARAMETER
corresponding_variable = input('corresponding: ')

if card_parameter in list_of_accetable_params:
    cardparam_valid = True
        match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
            case 'id':
                if corresponding_variable.digit() = True:
                    card_valid = True
                else:
                    print('id is incorrect format please try again')
            case 'type':
                if corresponding_variable in list_of_types:
                    card_valid = True
                else:
                    print('corresponding variable does not match, maybe use no capitals.')
            case 'atk':
                if corresponding_variable.digit() == True or corresponding_variable = '?':
                    card_valid = True
                else:
                    print('Attack value not correct format')
            case 'def':
                if corresponding_variable.digit() == True or corresponding_variable = '?':
                    card_valid = True
                else:
                    print('Attack value not correct format')



r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
    f'{card_parameter}' : f'{corresponding_variable}',})


def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent= 4)
    print(text)


if r.status_code == 200:
    jprint(r.json())





else:
    print('error')
