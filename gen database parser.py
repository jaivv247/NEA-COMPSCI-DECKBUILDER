import json
import requests
import os
from sys import argv
# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH


def jprint(obj):#THIS FUNCTION ALLOWS FOR PRINTING OF THE REQUEST SENT INTO THE API
     text = json.dumps(obj, sort_keys= True, indent= 4)
     print(text)

def error():
     print('Error has occured')
     match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
               case 'name':
                    print('Name is not correct please try again')
               case 'fname':
                    print('fname is not correct please try again')
               case 'id':
                    print('id is incorrect format please try again')
               case 'type':
                    print('corresponding variable does not match, use no capitals.')
               case 'atk':
                    print('Attack value not correct format')
               case 'def':
                    print('Defense value not correct format')
               case 'level':
                    print('level value is not a number please try again')
               case 'race':
                    print('Incorrect card race please try again')
               case 'attribute':
                    print('Attribute is not real please try again')
               case 'link':
                    print('link value is not a number please try again')
               case 'linkmarker':
                    print('Incorrect format please try again (make sure format is in word form and lowercase with dashes)')
               case 'scale':
                    print('scale value is not a number please try again')
               case 'cardset':
                    print('cardset not in set, please try again')
               case 'archetype':
                    print('Archetype not in set, please try again')
               case 'banlist':
                    print('The banlist for this format does not exist,try again')
               case 'format':
                    print('This format does not exist,try again')
               



script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist','format'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']



def card_parser(card_parameter , corresponding_variable):
     match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
          case 'name':
               return(True)
          case 'fname':
               return(True)
          case 'id':
               if corresponding_variable.isdigit() == True:
                    return(True)
               else:
                    print('id is incorrect format please try again')
          case 'type':
               Type_check = open("Types_for_check.txt",'r')
               for x in Type_check:
                    try:
                         if x == corresponding_variable:
                              return(True)
                              Type_check.close()
                    except:
                         print('corresponding variable does not match, use no capitals.')
          case 'atk':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
               else:
                    print('Attack value not correct format')
          case 'def':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
               else:
                    print('Defense value not correct format')
          case 'level':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 13:
                              return(True)
                    except:
                         print('Level is not between 1 and 12 please try again')
               else:
                    print('level value is not a number please try again')
          case 'race':
               if corresponding_variable in list_of_races:
                    return(True)
               else:
                    print('Incorrect card race please try again')
          case 'attribute':
               if corresponding_variable.upper() in list_of_attributes:
                    return(True)
               else:
                    print('Attribute is not real please try again')
          case 'link':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 7:
                              return(True)
                    except:
                         print('Link is not between 1 and 6 please try again')
               else:
                    print('link value is not a number please try again')
          case 'linkmarker':
               if corresponding_variable.lower() in list_of_linkmarkers:
                    return(True)
               else:
                    print('Incorrect format please try again (make sure format is in word form and lowercase with dashes)')
          case 'scale':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < -1 and int(corresponding_variable) > 14:
                              return(True)
                    except:
                         print('scale is not between 0 and 13 please try again')
               else:
                    print('scale value is not a number please try again')
          case 'cardset':
               cardset_check = open("Cardset_for_check.txt",'r')
               for x in cardset_check:
                    try:
                         if x == corresponding_variable:
                              return(True)
                              cardset_check.close()
                    except:
                         error()
          case 'archetype':
               Archetype_check = open("Archetypes_for_check.txt",'r')
               for x in Archetype_check:
                    try:
                         if x == corresponding_variable:
                              return(True)
                              Archetype_check.close()
                    except:
                         error()
          case 'banlist':
               if  corresponding_variable.upper in list_of_formats:
                    return(True)
               else:
                    error()
          case 'format':
               if  corresponding_variable.upper in list_of_formats:
                    return(True)
               else:
                    error()
               

    

card_parameter = input('what ygo api type thing are you searching for: ') # THIS LINE TAKES A PARAMETER
corresponding_variable = input('corresponding: ')                   
          
parse = card_parser(card_parameter)

if parse == True:
     r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
     f'{card_parameter}' : f'{corresponding_variable}',})

     if r.status_code == 200:
          jprint(r.json())

     else:
          print('error')
