#GLOBAL CONSTANTS AND LIBARIES
import json
import requests
import os
from sys import argv
looper_parse = 1
mode = ''


#import dearpygui.dearpygui as dpg
#dpg.create_context()
#dpg.create_viewport(title='Yu-gi-oh deck builder', width=600,height=300)

#with dpg.window(label='Main menu'):
     #dpg.add_text('Yugioh matrix')
     #dpg.add_button(label='Enter')
#dpg.setup_dearpygui()
#dpg.show_viewpoint()

#while dpg.is_dearpgui_running():

script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#MODE CHOOSE CODE INTO DBE OR PARSE FOR TESTS AND SUCH
def mode_maker():
     counter = 1
     while counter > 0 :
        list_of_modes = ['search','dbe','dev','stop']
        mode = input('what mode are we in: ')
        if mode not in list_of_modes:
            print('incorrect mode')
        else:
            return mode
        

#USER CREATION AND LOGIN SYSTEM
def read_accounts(): #reads the account file and splits the username and password of the user
     with open('Accounts_NEA.txt', 'r' ) as account_read:
          contents = account_read.readlines()
          new_contents = []

          for line in contents:
               fields = line.split(',')
               fields[1]=fields[1].rstrip()
               new_contents.append(fields)
          return new_contents


logins = read_accounts()

def login(): #login function checks if username and password are in the program
     counter = 1
     while counter > 0:
          ask_username = str(input('Username: '))
          ask_password = str(input('Password: '))

          logged_in = False

          for line in logins:
               if line[0] == ask_username and logged_in == False:
                    if line[1] == ask_password:
                         logged_in = True
          if logged_in == True:
               counter = 0
               print('Logged in successfully')
               global mode
               mode = mode_maker()
          else:
               print('Username/Password incorrect')

def create_accounts():#reads the existing accounts and creates a new account based on that
     with open ('Accounts_NEA.txt', 'a' ) as account_make:
          counter = 1
          while counter > 0:
               create_username = str(input('Input a username: '))
               create_password = str(input('Input a password: '))
               create_accounts()
               for line in logins:
                    if line[0] == create_username:
                         print('Username already exists please try again')
                    else:
                         account_make.write(f'{create_username}',f'{create_password}'+'\n')
     login()
          
check = False
while check == False :
     entry = input('''Welcome to the program:
                   click 1 to create an account
                   click 2 to login
                   : ''')
     if entry == '1':
          create_accounts()
          check = True
     elif entry == '2':
          login()
          check = True

def jprint(obj):#THIS FUNCTION ALLOWS FOR PRINTING OF THE REQUEST SENT INTO THE API
     text = json.dumps(obj, sort_keys= True, indent= 4)
     print(text)

def error(card_parameter): #this funtion is the mapped to each error and runs whenever an error occurs for the card parameters
     print('Error has occured')
     match card_parameter:
               case 'general':
                    print('Please try again')
                    looper_parse+=1
               case 'name':
                    print('Name is not correct please try again')
                    looper_parse_parse +=1
               case 'fname':
                    print('fname is not correct please try again')
                    looper_parse +=1
               case 'id':
                    print('id is incorrect format please try again')
                    looper_parse +=1
               case 'type':
                    print('corresponding variable does not match, use no capitals.')
                    looper_parse +=1
               case 'atk':
                    print('Attack value not correct format')
                    looper_parse +=1
               case 'def':
                    print('Defense value not correct format')
                    looper_parse +=1
               case 'level':
                    print('level value is not a number please try again')
                    looper_parse +=1
               case 'race':
                    print('Incorrect card race please try again')
                    looper_parse +=1
               case 'attribute':
                    print('Attribute is not real please try again')
                    looper_parse +=1
               case 'link':
                    print('link value is not a number please try again')
                    looper_parse +=1
               case 'linkmarker':
                    print('Incorrect format please try again (make sure format is in word form and lowercase with dashes)')
                    looper_parse +=1
               case 'scale':
                    print('scale value is not a number please try again')
                    looper_parse +=1
               case 'cardset':
                    print('cardset not in set, please try again')
                    looper_parse +=1
               case 'archetype':
                    print('Archetype not in set, please try again')
                    looper_parse +=1
               case 'banlist':
                    print('The banlist for this format does not exist,try again')
                    looper_parse +=1
               case 'format':
                    print('This format does not exist,try again')
                    looper_parse +=1
               

#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist','format'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']



# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH
looper_parse = 1
def card_parser(card_parameter , corresponding_variable):
     card_parameter = card_parameter.lower()
     match card_parameter:#SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLE
          case 'name':
               return(True)
               looper_parse = 0
          case 'fname':
               return(True)
               looper_parse = 0
          case 'id':
               if corresponding_variable.isdigit() == True:
                    return(True)
                    looper_parse = 0
               else:
                    error('id')
          case 'type':
               with open('Types_for_check.txt') as Type_check: # opens text file with all the types
                    #print('test')
                    datafile = Type_check.readlines() #creates a variable to store the list
                    length_of_file = len(datafile) #finds out the amount of lines in the file
                    len_counter = 0 # counter to show what line we are on
                    while len_counter < length_of_file: #whilst we havent looked at the whole file
                         #print('test')
                         for line in datafile: # for each line in the file
                               if corresponding_variable.upper() in line: # we check if the corresponding variable is in the list
                                     Type_check.close()
                                     looper_parse = 0
                                     len_counter = length_of_file +1# does this to stop the while loop whilst also not flag an error
                                     #print('test')
                                     return(True)
                               else:
                                     len_counter +=1 # increments if the current line is not the same as our variable
                    if len_counter == length_of_file: # if we have checked every line and we still havent gotten our variable then theres been an error
                         error('type')
          case 'atk':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
                    looper_parse = 0
               else:
                    error('atk')
          case 'def':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
                    looper_parse = 0
               else:
                    error('def')
          case 'level':
               if corresponding_variable.isdigit() == True:
                    if int(corresponding_variable) >= 0 and int(corresponding_variable) <= 13:
                         return(True)
                         looper_parse = 0
                    elif int(corresponding_variable) < 0 or int(corresponding_variable) > 13:
                         print('value is not in correct range')
                         error('general')
               else:
                    error('level')
          case 'race':
               if corresponding_variable.lower() in list_of_races:
                    return(True)
                    looper_parse = 0
               else:
                    error('race')
          case 'attribute':
               if corresponding_variable.upper() in list_of_attributes:
                    return(True)
                    looper_parse = 0
               else:
                    error('attribute')
          case 'link':
              if corresponding_variable.isdigit() == True:
                    if int(corresponding_variable) > 0 and int(corresponding_variable) <=6:
                         return(True)
                         looper_parse = 0
                    elif int(corresponding_variable) < 0 or int(corresponding_variable) > 6:
                         print('value is not in correct range')
                         error('general')
              else:
                    error('link')
          case 'linkmarker':
               if corresponding_variable.lower() in list_of_linkmarkers:
                    return(True)
                    looper_parse = 0
               else:
                    error('linkmarker')
          case 'scale':
                 if corresponding_variable.isdigit() == True:
                    if int(corresponding_variable) >= 0 and int(corresponding_variable) <= 14:
                         return(True)
                         looper_parse = 0
                    elif int(corresponding_variable) < 0 or int(corresponding_variable) > 14:
                         print('value is not in correct range')
                         error('general')
                 else:
                         error('scale')
          case 'cardset':
                    with open('Cardset_for_check.txt') as Type_check:
                         datafile = Type_check.readlines()
                         length_of_file = len(datafile) 
                         len_counter = 0
                    while len_counter < length_of_file:
                         for line in datafile:
                               if corresponding_variable.upper() in line:
                                     Type_check.close()

                                     looper_parse = 0
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
                                        looper_parse = 0
                                        len_counter = length_of_file +1
                                        return(True)
                                   else:
                                        len_counter +=1
                         if len_counter == length_of_file:
                              error('archetype')
          case 'banlist':
               if corresponding_variable.upper() in list_of_formats:
                    return(True)
                    looper_parse = 0
               else:
                    error('banlist')
          case 'format':
               if  corresponding_variable.upper() in list_of_formats:
                    return(True)
                    looper_parse = 0
               else:
                    error('format')
     if card_parameter not in list_of_acceptable_params:
          print('Parameter not parasable')
          error('general')
               
#DATABASE PARSE CALL CODE
def database_call():                 
          try:
               r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
               f'{card_parameter}' : f'{corresponding_variable}',})

               if r.status_code == 200:
                    jprint(r.json())
                    looper_parse = 0
               else:
                    print('error')
          except:
               print('Error has occured in database parser')

          counter = 1
          while counter > 0:
               again = input('''Would you like to search again?
               click 1 to search again 
               click 2 to stop search
               : ''')
               global mode
               if again == '1':
                    mode ='search'
               if again == '2':
                    mode = 'stop'
                    break
               if again != '1' or again != '2':
                    print('Incorrect repsonse')





#actual search for cards
while looper_parse > 0 and mode == 'search':
     card_parameter = input('what ygo api type thing are you searching for: ')
     corresponding_variable = input('corresponding: ')
     parse = card_parser(card_parameter,corresponding_variable)
     if parse == True:
          database_call()







