#GLOBAL CONSTANTS AND LIBARIES
import json
import requests
import os
from sys import argv
import dearpygui.dearpygui as dpg
import time

global mode
mode = ''
#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_modes = ['search','dbe','dev','stop','create','menu']
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']


script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#Deck building environment
def create_deck_file(deck_name, username):
     user_folder = os.path.join(os.getcwd(), username)
     if not os.path.exists(user_folder):
          print(f"User folder '{username}' does not exist. Creating folder...")
          os.makedirs(user_folder)
     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     with open(deck_file_path, "w") as deck_file:
          json.dump([], deck_file)
          print(f"Deck '{deck_name}' created successfully.")

def inital_search_func(search):
     search_data = json.loads(j_compact_print(search.json()))

     if "data" not in search_data:
          print("No valid card data found.")
          return

     keys_to_extract = ['name', 'type']

     extracted_data = []
     for card in search_data["data"]:
          filtered_card = {key: card[key] for key in keys_to_extract if key in card}
          extracted_data.append(filtered_card)

     j_pretty_print(extracted_data)
     return extracted_data


def on_click_search_func(search):
     search_data = json.loads(j_compact_print(search.json()))

     if "data" not in search_data:
          print("No valid card data found.")
          return

     keys_to_extract = ['id', 'name', 'type', 'desc', 'atk', 'def', 'level', 'attribute', 'archetype', 'race']

     extracted_data = []
     for card in search_data["data"]:
          filtered_card = {key: card[key] for key in keys_to_extract if key in card}
          extracted_data.append(filtered_card)

     j_pretty_print(extracted_data)
     return extracted_data

def deck_size_check(deck_name):
     

def save_card_to_deck(deck_name, username, card_data):
     with open(f'{deck_name}.json','w') as deck file:
          counter_of_number
     #search_dictionary = search.json()



#THESE FUNCTIONS ALLOW FOR PRINTING OF THE REQUEST SENT INTO THE API
def j_pretty_print(obj):
     text = json.dumps(obj, indent= 4)
     print(text)
     return text
def j_compact_print(obj):
     text = json.dumps(obj,separators=(',',':'))
     return text


#DATABASE PARSE CALL CODE
def database_call(search_dict):                 
          try:
               r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php',params=search_dict)
               if r.status_code == 200:
                    j_pretty_print(r.json())
                    return r
               else:
                    print(f'error:{r.status_code}')
          except:
               print('error')

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
               case _: 
                    print('no parameter passed, try again')
          

# THIS IS A BETA VERSION OF THE GENERIC CARD SEARCH
def card_parser_validator(card_parameter , corresponding_variable):
     card_parameter = card_parameter.lower()
     #SWITCH CASE TO VALIDATE THE PARAMETERS AND CORRESPONDING VARIABLES
     match card_parameter:
          case 'name':
               return(True)
          case 'fname':
               return(True)
          case 'id':
               if corresponding_variable.isdigit() == True:
                    return(True)
               else:
                    error('id')
                    return False
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
                                   len_counter = length_of_file +1# does this to stop the while loop whilst also not flag an error
                                   #print('test')
                                   return(True)
                              else:
                                   len_counter +=1 # increments if the current line is not the same as our variable
                    if len_counter == length_of_file: # if we have checked every line and we still havent gotten our variable then theres been an error
                         error('type')
                         return False
          case 'atk':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
                    
               else:
                    error('atk')
                    return False
          case 'def':
               if corresponding_variable.isdigit() == True or corresponding_variable == '?':
                    return(True)
               else:
                    error('def')
                    return False
          case 'level':
               if corresponding_variable.isdigit() == True:
                    if int(corresponding_variable) >= 0 and int(corresponding_variable) <= 13:
                         return(True)
                    elif int(corresponding_variable) < 0 or int(corresponding_variable) > 13:
                         print('value is not in correct range')
                         error('general')
                         return False
               if not corresponding_variable.isdigit() or not (0 <= int(corresponding_variable) <= 13):
                    error('level')
                    return False
          case 'race':
               if corresponding_variable.lower() in list_of_races:
                    return(True)
               else:
                    error('race')
          case 'attribute':
               if corresponding_variable.upper() in list_of_attributes:
                    return(True)
               else:
                    error('attribute')
          case 'link':
               if corresponding_variable.isdigit() == True:
                         if int(corresponding_variable) > 0 and int(corresponding_variable) <=6:
                              return(True)
                         elif int(corresponding_variable) < 0 or int(corresponding_variable) > 6:
                              print('value is not in correct range')
                              error('general')
                              return False
               else:
                         error('link')
                         return False
          case 'linkmarker':
               if corresponding_variable.lower() in list_of_linkmarkers:
                    return(True)
               else:
                    error('linkmarker')
                    return False
          case 'scale':
               if corresponding_variable.isdigit() == True:
                    if int(corresponding_variable) >= 0 and int(corresponding_variable) <= 14:
                         return(True)
                    elif int(corresponding_variable) < 0 or int(corresponding_variable) > 14:
                         print('value is not in correct range')
                         error('general')
                         return False
               else:
                         error('scale')
                         return False
          case 'cardset':
                    with open('Cardset_for_check.txt') as Type_check:
                         datafile = Type_check.readlines()
                         length_of_file = len(datafile) 
                         len_counter = 0
                    while len_counter < length_of_file:
                         for line in datafile:
                              if corresponding_variable.upper() in line:
                                   Type_check.close()
                                   len_counter = length_of_file +1
                                   return(True)
                              else:
                                   len_counter +=1
                    if len_counter == length_of_file:
                         error('cardset')
                         return False
          case 'archetype':
                    with open('Archetypes_for_check.txt') as Type_check:
                         datafile = Type_check.readlines()
                         length_of_file = len(datafile) 
                         len_counter = 0
                         while len_counter < length_of_file:
                              for line in datafile:
                                   if corresponding_variable.upper() in line:
                                        Type_check.close()
                                        
                                        len_counter = length_of_file +1
                                        return(True)
                                   else:
                                        len_counter +=1
                         if len_counter == length_of_file:
                              error('archetype')
                              return False
          case 'banlist':
               if corresponding_variable.upper() in list_of_formats:
                    return(True)
               else:
                    error('banlist')
                    return False
     if card_parameter not in list_of_acceptable_params:
          print('Parameter not parasable')
          error('general')
          return False

def mode_stop():
     quit()

def mode_dbe(call_return):
     #print('Mode was changed')
     inital_search_func(call_return)
     #on_click_search_func(call_return)
     # add = save_card_to_deck(deckname, username, call_return)

     # if add == False:
     #      mode = 'create'

     counter = 1
     while counter > 0:
          again = input('''Would you like to search again?
          click 1 to search again 
          click 2 to stop
          : ''')

          if again == '1':
               mode_search()
               counter = 0
          elif again == '2':
               mode_stop()
               counter = 0
          else:
               print('incorrect response')


def mode_search():
     search_dict = {}
     parameter_number = input('how many parameters would you like to pass?: ')
     while not parameter_number.isdigit():
               print('Error input was not a number')
               parameter_number = input('how many parameters would you like to pass?: ')

     parameter_number = int(parameter_number)

     for _ in range(parameter_number):
          card_parameter = input('Param: ') # takes in parameter for search
          corresponding_variable = input('Variable: ') # the variable correspoding to the parameter that the user wants to actually search for like a specific card type or card.
          validate = card_parser_validator(card_parameter,corresponding_variable)
          if validate == True:
               search_dict[card_parameter] = corresponding_variable
          elif validate == False:
               parameter_number +=1
     if search_dict:
          call_return = database_call(search_dict)
     else:
          print('No valid parameters provided. Please enter valid search terms.')
     counter = 1
     while counter > 0:
          again = input('''Would you like to search again?
          click 1 to search again 
          click 2 to begin deck building
          click 3 to stop
          : ''')

          if again == '1':
               mode_search()
               counter = 0
          elif again == '2':
               mode_dbe(call_return)
               counter = 0
          elif again == '3':
               mode_stop()
               counter = 0
          else:
               print('incorrect response')


def mode_create(username):
     deck_name = input('what is the name of your deck: ')

     user_folder = os.path.join(os.getcwd(), username)

     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     if os.path.exists(deck_file_path):
        print(f"Deck '{deck_name}' already exists.")
        mode_create(username)
     else:
          create_deck_file(deck_name,username)
          mode_search()



#MODE CHOOSE CODE INTO DBE OR PARSE FOR TESTS AND SUCH
def mode_maker():
     counter = 1
     while counter > 0 :
          mode = input('what mode are we in: ').lower()
          if mode not in list_of_modes:
               print('incorrect mode')
          else:
               match mode:
                    case 'search':
                         mode_search()
                    case 'dbe':
                         mode_dbe()
                    #'dev':
                         # mode_dev()
                    case 'stop':
                         mode_stop()
                    case 'create':
                         mode_create(username)
                    #'menu':
                         #mode_menu()

               return 
     

#USER CREATION AND LOGIN SYSTEM
def read_accounts(): #reads the account file and splits the username and password of the user
     if not os.path.exists('Accounts_NEA.txt'):
          with open('Accounts_NEA.txt', 'w') as f:  # Create an empty file if it doesn't exist
               pass
          read_accounts()
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
          global username
          global password
          username = str(input('username: '))
          password = str(input('password: '))
          logged_in = False
          logins = read_accounts()
          #print(logins)
          for line in logins:
               #print(line[0])
               if line[0] == username and logged_in == False:
                    if line[1] == password:
                         logged_in = True
          if logged_in == True:
               counter = 0
               #dpg.add_text('Logged in successfully')
               print('Logged in successfully')
               mode_maker()
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

            user_folder = os.path.join(os.getcwd(), create_username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
                print(f'Folder "{create_username}" created successfully.')
            else:
                print(f'Folder "{create_username}" already exists.')
                      
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



          







# ##GUI set up code

# dpg.create_context()
# dpg.configure_app(docking=True, docking_space=True, load_init_file="custom_layout.ini") # must be called before create_viewport
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
     



# dpg.add_window(label="Left", tag=left_window,show=True,no_move=True)
#      #dpg.set_item_pos('left_window',pos=(1000,0))
# dpg.add_window(label="Right", tag=right_window,show=True,no_move=True)
# dpg.add_window(label="Top", tag=top_window,show=True,no_move=True)
# dpg.add_window(label="Bottom", tag=bottom_window,show=True,no_move=True)
# with dpg.window(label="Center", tag=center_window,show=True,no_move=True):
#      dpg.add_input_text(label='Select window',on_enter=True,callback=window_selection,tag='select window')
#      dpg.add_button(label='Click',callback=window_selection)
     



# #dpg.set_primary_window('center_window',True)




# # main loop
# dpg.show_viewport()
# while dpg.is_dearpygui_running():
#     dpg.render_dearpygui_frame()  

# dpg.destroy_context()
