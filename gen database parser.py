import json
import requests
import os
from sys import argv
# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH


def jprint(obj):#THIS FUNCTION ALLOWS FOR PRINTING OF THE REQUEST SENT INTO THE API
     text = json.dumps(obj, sort_keys= True, indent= 4)
     print(text)


script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist','format'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']


cardparam_valid = False
cardvariable_valid = False
while cardvariable_valid == False and cardparam_valid == False:
     card_parameter = input('what ygo api type thing are you searching for: ') # THIS LINE TAKES A PARAMETER
     corresponding_variable = input('corresponding: ')
     if card_parameter in list_of_acceptable_params:#PARAMETER VALIDATION
          cardparam_valid = True
          match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
               case 'name':
                    cardvariable_valid = True
               case 'fname':
                    cardvariable_valid = True
               case 'id':
                    if corresponding_variable.isdigit() == True:
                         cardvariable_valid = True
                    else:
                         print('id is incorrect format please try again')
               case 'type':
                    Type_check = open("Types_for_check.txt",'r')
                    for x in Type_check:
                         try:
                              if x == corresponding_variable:
                                   cardvariable_valid = True
                                   Type_check.close()
                         except:
                              print('corresponding variable does not match, use no capitals.')
               case 'atk':
                    if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                         cardvariable_valid = True
                    else:
                         print('Attack value not correct format')
               case 'def':
                    if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                         cardvariable_valid = True
                    else:
                         print('Defense value not correct format')
               case 'level':
                    if corresponding_variable.isdigit() == True:
                         try:
                              if int(corresponding_variable) < 0 and int(corresponding_variable) > 13:
                                   cardvariable_valid = True
                         except:
                              print('Level is not between 1 and 12 please try again')
                    else:
                         print('level value is not a number please try again')
               case 'race':
                    if corresponding_variable in list_of_races:
                         cardvariable_valid = True
                    else:
                         print('Incorrect card race please try again')
               case 'attribute':
                    if corresponding_variable.upper() in list_of_attributes:
                         cardvariable_valid = True
                    else:
                         print('Attribute is not real please try again')
               case 'link':
                    if corresponding_variable.isdigit() == True:
                         try:
                              if int(corresponding_variable) < 0 and int(corresponding_variable) > 7:
                                   cardvariable_valid = True
                         except:
                              print('Link is not between 1 and 6 please try again')
                    else:
                         print('link value is not a number please try again')
               case 'linkmarker':
                    if corresponding_variable.lower() in list_of_linkmarkers:
                         cardvariable_valid = True
                    else:
                         print('Incorrect format please try again (make sure format is in word form and lowercase with dashes)')
               case 'scale':
                    if corresponding_variable.isdigit() == True:
                         try:
                              if int(corresponding_variable) < -1 and int(corresponding_variable) > 14:
                                   cardvariable_valid = True
                         except:
                              print('scale is not between 0 and 13 please try again')
                    else:
                         print('scale value is not a number please try again')
               case 'cardset':
                    cardset_check = open("Cardset_for_check.txt",'r')
                    for x in cardset_check:
                         try:
                              if x == corresponding_variable:
                                   cardvariable_valid = True
                                   cardset_check.close()
                         except:
                              print('Cardset is not in database, check name and try again')
               case 'archetype':
                    Archetype_check = open("Archetypes_for_check.txt",'r')
                    for x in Archetype_check:
                         try:
                              if x == corresponding_variable:
                                   cardvariable_valid = True
                                   Archetype_check.close()
                         except:
                              print('Cardset is not in database, check name and try again')
               case 'banlist':
                    if  corresponding_variable.upper in list_of_formats:
                         cardvariable_valid = True
                    else:
                         print('The banlist for this format does not exist,try again')
               case 'format':
                    if  corresponding_variable.upper in list_of_formats:
                         cardvariable_valid = True
                    else:
                         print('This format does not exist,try again')
               



if cardvariable_valid == True:
     r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
     f'{card_parameter}' : f'{corresponding_variable}',})

     if r.status_code == 200:
          jprint(r.json())

     else:
          print('error')
