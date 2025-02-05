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
               case 'name':
                    print('Name is not correct please try again')
                    looper +=1
               case 'fname':
                    print('fname is not correct please try again')
                    looper +=1
               case 'id':
                    print('id is incorrect format please try again')
                    looper +=1
               case 'type':
                    print('corresponding variable does not match, use no capitals.')
                    looper +=1
               case 'atk':
                    print('Attack value not correct format')
                    looper +=1
               case 'def':
                    print('Defense value not correct format')
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
               return(True)
               looper = 0
          case 'fname':
               return(True)
               looper = 0
          case 'id':
               if corresponding_variable.isdigit() == True:
                    return(True)
                    looper = 0
               else:
                    error('id')
          case 'type':
               with open('Types_for_check.txt') as Type_check: # opens text file with all the types
                    datafile = Type_check.readlines() #creates a variable to store the list
                    length_of_file = len(datafile) #finds out the amount of lines in the file
                    len_counter = 0 # counter to show what line we are on
                    while len_counter < length_of_file: #whilst we havent looked at the whole file
                         for line in datafile: # for each line in the file
                               if corresponding_variable.upper() in line: # we check if the corresponding variable is in the list
                                     Type_check.close()
                                     looper = 0
                                     len_counter = length_of_file +1 # does this to stop the while loop whilst also not flag an error
                                     return(True)
                               else:
                                     len_counter +=1 # increments if the current line is not the same as our variable
                    if len_counter == length_of_file: # if we have checked every line and we still havent gotten our variable then theres been an error
                         error('type')
          case 'atk':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
                    looper = 0
               else:
                    error('atk')
          case 'def':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
                    looper = 0
               else:
                    error('def')
          case 'level':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 13:
                              return(True)
                              looper = 0
     
                    except:
                         print('level not between 1-12')
                         error('general')
               else:
                    error('level')
          case 'race':
               if corresponding_variable in list_of_races:
                    return(True)
                    looper = 0
               else:
                    error('race')
          case 'attribute':
               if corresponding_variable.upper() in list_of_attributes:
                    return(True)
                    looper = 0
               else:
                    error('attribute')
          case 'link':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < 0 and int(corresponding_variable) > 7:
                              return(True)
                              looper = 0
     
                    except:
                         print('Link is not between 1 and 6 please try again')
                         error('general')
               else:
                    error('link')
          case 'linkmarker':
               if corresponding_variable.lower() in list_of_linkmarkers:
                    return(True)
                    looper = 0
               else:
                    error('linkmarker')
          case 'scale':
               if corresponding_variable.isdigit() == True:
                    try:
                         if int(corresponding_variable) < -1 and int(corresponding_variable) > 14:
                              return(True)
                              looper = 0
     
                    except:
                         print('Scale value is not between 0 and 13')
                         error('general')
               else:
                    print('scale')
          case 'cardset':
                    with open('Cardset_for_check.txt') as Type_check:
                         datafile = Type_check.readlines()
                         length_of_file = len(datafile) 
                         len_counter = 0
                    while len_counter < length_of_file:
                         for line in datafile:
                               if corresponding_variable.upper() in line:
                                     Type_check.close()
                                     looper = 0
                                     len_counter = length_of_file +1
                                     return(True)
                               else:
                                     len_counter +=1
                    if len_counter == length_of_file:
                         error('cardset')
          case 'archetype':
                  with open('Archetypes_for_check.txt') as Type_check:
                    datafile = Type_check.readlines()
                    length_of_file = len(datafile) 
                    len_counter = 0
                    while len_counter < length_of_file:
                         for line in datafile:
                               if corresponding_variable.upper() in line:
                                     Type_check.close()
                                     looper = 0
                                     len_counter = length_of_file +1
                                     return(True)
                               else:
                                     len_counter +=1
                    if len_counter == length_of_file:
                         error('archetype')
          case 'banlist':
               if  corresponding_variable.upper in list_of_formats:
                    return(True)
                    looper = 0
               else:
                    error('banlist')
          case 'format':
               if  corresponding_variable.upper in list_of_formats:
                    return(True)
                    looper = 0
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
     except:
          print('Error has occured in database parser')

     
