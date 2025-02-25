#GLOBAL CONSTANTS AND LIBARIES
import json
import requests
import os
from sys import argv
import dearpygui.dearpygui as dpg
import time

looper_parse = 1
mode = ''
#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_modes = ['search','dbe','dev','stop']
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist','format'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']

script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#MODE CHOOSE CODE INTO DBE OR PARSE FOR TESTS AND SUCH
def mode_maker():
     counter = 1
     while counter > 0 :
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
               #print(fields)
               fields[1]=fields[1].rstrip()
               new_contents.append(fields)
          return new_contents

#login function checks if username and password are in the program
def login():#(sender,data):
     counter = 1
     while counter > 0:
          #ask_username = dpg.add_input_text(label='Username: ',default_value='Type here')
          #ask_password = dpg.add_input_text(label='Password: ',default_value='Type here')
          ask_username = str(input('username: '))
          ask_password = str(input('password: '))
          logged_in = False
          logins = read_accounts()
          #print(logins)
          for line in logins:
               #print(line[0])
               if line[0] == ask_username and logged_in == False:
                    if line[1] == ask_password:
                         logged_in = True
          if logged_in == True:
               counter = 0
               #dpg.add_text('Logged in successfully')
               print('Logged in successfully')
               global mode
               mode = mode_maker()
          else:
               #dpg.add_text('Username/Password incorrect')
               print('Username/Password incorrect')

#reads the existing accounts and creates a new account based on that
def create_accounts():#(sender,data):
     counter = 1
     while counter > 0:
        create_username = str(input('Input a username: '))
        create_password = str(input('Input a password: '))

        username_exists = False
        logins = read_accounts()
        for line in logins:
            if line[0] == create_username:
                username_exists = True
                break
        if username_exists:
            print('Username already exists, please choose a different one')
        else:
            with open('Accounts_NEA.txt', 'a') as account_make:
                account_make.write(f'{create_username},{create_password}\n')
            print('Account created successfully')
            counter = -1
     login()


#terminal side UI for test

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
     #SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLES
     match card_parameter:
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
               


def saveToDecklist():
     #json manipulation
     # adds to global deck



#DATABASE PARSE CALL CODE
def database_call():                 
          try:
               r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params={
               f'{card_parameter}' : f'{corresponding_variable}'})

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
                    return 1
               if again == '2':
                    mode = 'stop'
                    return r
               else:
                    print('incorrect response')
                    

while mode == 'stop':
     break


#actual search for cards
while looper_parse > 0 and mode == 'search':
     card_parameter = input('what ygo api type thing are you searching for: ')
     corresponding_variable = input('corresponding: ')
     parse = card_parser(card_parameter,corresponding_variable)
     if parse == True:
          var = database_call()
     

#GUI set up code




# dpg.create_context()
# # dpg.configure_app(docking=True, docking_space=True, load_init_file="custom_layout.ini") # must be called before create_viewport
# dpg.create_viewport(title='Yugioh duel matrix',width=1920,height=1080)
# dpg.setup_dearpygui()

# # generate IDs - the IDs are used by the init file, they must be the
# #                same between sessions
# left_window = dpg.generate_uuid()
# right_window = dpg.generate_uuid()
# top_window = dpg.generate_uuid()
# bottom_window = dpg.generate_uuid()
# center_window = dpg.generate_uuid()
# param =''




# def hide_window(param):
#      dpg.configure_item(param,show=True)

# def show_window(param):
#      dpg.configure_item(param,show=True)


# def window_selection(sender,data):
#      print(dpg.get_value('select window'))
#      param= dpg.get_value('select window')
#      hide_window(dpg.get_value('select window'))
#      time.sleep(5)
#      show_window(dpg.get_value('select window'))
     



# with dpg.window(label="Left", tag=left_window,show=True,no_move=True):
#      dpg.set_item_pos('left_window',pos=(1000,0))
# dpg.add_window(label="Right", tag=right_window,show=True,no_move=True)
# dpg.add_window(label="Top", tag=top_window,show=True,no_move=True)
# dpg.add_window(label="Bottom", tag=bottom_window,show=True,no_move=True)
# with dpg.window(label="Center", tag=center_window,show=True,no_move=True):
#      dpg.add_input_text(label='Select window',on_enter=True,callback=window_selection,tag='select window')
#      dpg.add_button(label='Click',callback=window_selection)
     



# dpg.set_primary_window('center_window',True)




# # main loop
# dpg.show_viewport()
# while dpg.is_dearpygui_running():
#     dpg.render_dearpygui_frame()  

# dpg.destroy_context()
