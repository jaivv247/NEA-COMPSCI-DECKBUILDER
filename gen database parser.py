import json
import requests
import os
from sys import argv
# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH
looper = 1

def jprint(obj):#THIS FUNCTION ALLOWS FOR PRINTING OF THE REQUEST SENT INTO THE API
     text = json.dumps(obj, sort_keys= True, indent= 4)
     print(text)

def error(card_parameter): #this funtion is the mapped to each error and runs whenever an error occurs for the card parameters
     print('Error has occured')
     match card_parameter:
               case 'general':
                    print('Please try again')
                    looper +=1
               case 'id':
                    print('id is incorrect format, check if id is 8 numbers, please try again')
                    looper +=1
               case 'type':
                    print('corresponding variable does not match, use no capitals.')
                    looper +=1
               case 'atk':
                    print('Attack value not correct format')
                    looper +=1
               case 'def':
                    looper +=1
               case 'level':
                    print('level value is not a number please try again')
                    looper +=1
               case 'race':
                    print('Incorrect card race please try again')
                    looper +=1
               case 'attribute':
                    print('Attribute is not real please try again')
                    looper +=1
               case 'link':
                    print('link value is not a number please try again')
                    looper +=1
               case 'linkmarker':
                    print('Incorrect format please try again (make sure format is in word form and lowercase with dashes)')
                    looper +=1
               case 'scale':
                    print('scale value is not a number please try again')
                    looper +=1
               case 'cardset':
                    print('cardset not in set, please try again')
                    looper +=1
               case 'archetype':
                    print('Archetype not in set, please try again')
                    looper +=1
               case 'banlist':
                    print('The banlist for this format does not exist,try again')
                    looper +=1
               case 'format':
                    print('This format does not exist,try again')
                    looper +=1
               



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
               looper = 0
               return (True)
          case 'fname':
               looper = 0
               return (True)
          case 'id':
               if corresponding_variable.isdigit() == True and len(corresponding_variable)== 8:
                    looper = 0
                    return (True)
               else:
                    error('id')
          case 'type':
               Type_check = open("Types_for_check.txt",'r')
               tracker = 0
               flag = False
               for x in Type_check:
                    try:
                         if x == corresponding_variable:
                              Type_check.close()
                              looper = 0
                              return (True)
                    except:
                         tracker +=1
                         if tracker >= 29:
                              Type_check.close
                              flag = True
               if flag == True:
                    error('type')
          case 'atk':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    looper = 0
                    return (True)
               else:
                    error('atk')
          case 'def':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    looper = 0
                    return (True)
               else:
                    error('def')
          case 'level':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 13: 
                              looper = 0
                              return(True)
                    except:
                         print('level not between 1-12')
                         error('general')
               else:
                    error('level')
          case 'race':
               if corresponding_variable in list_of_races:
                    looper = 0
                    return(True)
               else:
                    error('race')
          case 'attribute':
               if corresponding_variable.upper() in list_of_attributes:
                    looper = 0
                    return(True)
               else:
                    error('attribute')
          case 'link':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 7:
                              looper = 0
                              return(True)
                    except:
                         print('Link is not between 1 and 6 please try again')
                         error('general')
               else:
                    error('link')
          case 'linkmarker':
               if corresponding_variable.lower() in list_of_linkmarkers:
                    looper = 0
                    return(True)
               else:
                    error('linkmarker')
          case 'scale':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < -1 and int(corresponding_variable) > 14:
                              looper = 0
                              return(True)
                    except:
                         print('Scale value is not between 0 and 13')
                         error('general')
               else:
                    print('scale')
          case 'cardset':
               cardset_check = open("Cardset_for_check.txt",'r')
               for x in cardset_check:
                    try:
                         if x == corresponding_variable:
                              cardset_check.close()
                              looper = 0
                              return(True)
                    except:
                         error('cardset')
          case 'archetype':
               Archetype_check = open("Archetypes_for_check.txt",'r')
               for x in Archetype_check:
                    try:
                         if x == corresponding_variable:
                              
                              Archetype_check.close()
                              looper = 0
                              return(True)
                    except:
                         error('archetype')
          case 'banlist':
               if  corresponding_variable.upper in list_of_formats:
                    looper = 0
                    return(True)
               else:
                    error('banlist')
          case 'format':
               if  corresponding_variable.upper in list_of_formats:
                    looper = 0
                    return(True)
               else:
                    error('format')
     if card_parameter not in list_of_acceptable_params:
          print('Parameter not parasable')
          error('general')
               

    
while looper > 0:
     card_parameter = input('what ygo api type thing are you searching for: ')
     corresponding_variable = input('corresponding: ')                   
          
     try:
          parse = card_parser(card_parameter,corresponding_variable)
          if parse == True:
               r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
               f'{card_parameter}' : f'{corresponding_variable}',})

               if r.status_code == 200:
                    jprint(r.json())
                    looper = 0
               else:
                    print('error')
                    error('general')
     except:
          print('Error has occured in database parser')
