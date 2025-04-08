#GLOBAL CONSTANTS AND LIBARIES
import json
import requests
import os
from sys import argv
import dearpygui.dearpygui as dpg
import time
from collections import Counter
global mode
global deck_name
mode = ''
global deck_legal
deck_legal = True

#ALL THE STRINGS TO CHECK VARIABLES AGAINST
list_of_extradeck_monsters = ['FUSION MONSTER','LINK MONSTER','PENDULUM EFFECT FUSION MONSTER','SYNCHRO MONSTER','SYNCHRO PENDULUM EFFECT MONSTER','SYNCHRO TUNER MONSTER','XYZ MONSTER','XYZ PENDULUM EFFECT MONSTER']
list_of_modes = ['search','dbe','stop','create','open']
list_of_races = ['aqua','beast','beast-warrior','creator-god','cyberse','dinosaur','divine-beast','dragon','fairy','fiend','fish','insect','machine','plant','psychic','pyro','reptile','rock','sea serpent','spellcaster','thunder','warrior','winged beast','wyrm','zombie','normal','field','equip','continuous','quick-play','ritual','normal','continuous','counter']
list_of_acceptable_params = ['name','fname','id','type','atk','def','level','race','attribute','link','linkmarker','scale','cardset','archetype','banlist'] #LIST OF ACCEPTABLE PARAMETERS
list_of_attributes = ['DARK','DIVINE','EARTH','FIRE','LIGHT','WATER','WIND']
list_of_linkmarkers = ['top', 'bottom', 'left', 'right', 'bottom-left', 'bottom-right', 'top-left', 'top-right']
list_of_formats = ['TCG','OCG','GOAT']


script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file to ignore path to file, only needs to change path from file
os.chdir(script_directory)

#THESE FUNCTIONS ALLOW FOR PRINTING OF THE REQUEST SENT INTO THE API
def j_pretty_print(obj):
     text = json.dumps(obj, indent= 4)
     print(text)
     return text
def j_compact_print(obj):
     text = json.dumps(obj,separators=(',',':'))
     return text

#Deck building environment
#deck creation function
def create_deck_file(deck_name, username):
     user_folder = os.path.join(os.getcwd(), username)
     if not os.path.exists(user_folder):
          print(f"User folder '{username}' does not exist. Creating folder...")
          os.makedirs(user_folder)
     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     with open(deck_file_path, "w") as deck_file:
          json.dump([], deck_file)
          print(f"Deck '{deck_name}' created successfully.")

#inital search function
def inital_search_func(search):
     search_data =json.loads(j_compact_print(search.json()))
     #print(search_data)
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

#eextra information search function
def on_click_search_func(search):
     search_data =j_compact_print(search.json())

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


#save function
def save_card_to_deck(card_data, username,deck_name):
     user_folder = os.path.join(os.getcwd(), username)
     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")

     if not os.path.exists(deck_file_path):
          print(f"Deck '{deck_name}' does not exist. Creating new deck file...")
          create_deck_file(deck_name, username)
     
     try:
          with open(deck_file_path, 'r') as deck_file:
               try:
                    deck = json.load(deck_file)
                    if not isinstance(deck, list):
                              deck = []
               except json.JSONDecodeError:
                    deck = []
     except FileNotFoundError:
          deck = []
     
     deck.append(card_data.json())
     #deck.append(json.dumps(card_data.json())) #I only know 50% of why this line works
     with open(deck_file_path, 'w') as deck_file:
          json.dump(deck, deck_file, indent=4)
     print(f'Card added successfully to {deck_name}.json')

def delete_card_from_deck(username,deck_name,card_name_to_remove):
     user_folder = os.path.join(os.getcwd(), username)
     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     try:
          with open(deck_file_path, 'r') as deck_file:
               deck = json.load(deck_file)
          card_found = False
          
          for card in deck:
               if 'data' in card and isinstance(card['data'], list):
                    for i, card_data in enumerate(card['data']):
                         if card_data.get('name', '').lower() == card_name_to_remove.lower():
                              del card['data'][i]
                              card_found = True
                              break
               if card_found:
                    break
          
          deck = [card for card in deck if card.get('data')]

          with open(deck_file_path, 'w') as deck_file:
               json.dump(deck, deck_file, indent=4)

          if card_found:
               print(f"Removed one instance of '{card_name_to_remove}' from the deck.")
          else:
               print(f"Card '{card_name_to_remove}' not found in '{deck_name}'.")
     except (FileNotFoundError, json.JSONDecodeError):
          print("Error: Could not open or read the deck file.")

#limit checker
def deck_check(username, deck_name):
     user_folder = os.path.join(os.getcwd(), username)
     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     extracted_data_name = []
     extracted_data_type = []
     extra_deck = []
     main_deck = []
     global deck_legal
     deck_legal = True

     try:
          with open(deck_file_path, 'r') as deck_file:
               deck = json.load(deck_file)

          if deck: 
               print('There are cards in the deck')

               for card in deck:
                    if 'data' in card and isinstance(card['data'], list):
                         for card_data in card['data']:
                              card_name = card_data.get('name', 'Unknown')
                              extracted_data_name.append(card_name)
                              card_type = card_data.get('type','Unknown')
                              extracted_data_type.append(card_type)
                    else: 
                         print("Warning: Invalid card format")

               full_list = list(zip(extracted_data_name, extracted_data_type))

               # print('----- FULL 2D ARRAY------')
               # print(full_list)
               # print('---- NAMES ONLY-----')
               # print(extracted_data_name)

               card_counts = Counter(extracted_data_name)
               amount_in_deck = len(extracted_data_name)

               for card, count in card_counts.items():
                    if count > 3:
                         deck_legal = False
                         reason = 'too many of card'

               if amount_in_deck > 75 :
                    deck_legal = False
                    reason = 'too many in total'
                    
               if amount_in_deck  < 40 :
                    deck_legal = False
                    reason = 'too little in total'

               for name,type_ in full_list:
                    if type_.upper() in list_of_extradeck_monsters:
                         extra_deck.append((name,type_))
                    else:
                         main_deck.append((name,type_))
               
               print('"\n--- Main Deck Cards ---"')
               for card in main_deck:
                    print(card[0])
               
               print('"\n--- Extra Deck Cards ---"')
               for card in extra_deck:
                    print(card[0])
               
               if len(main_deck) > 60 or len(main_deck) < 40:
                    deck_legal = False
                    reason = 'card number in main invalid'
               if len(extra_deck) > 15:
                    deck_legal = False
                    reason = 'card number in extra invalid'
          else:
               print("Deck is empty.")
               mode_search()
     except (FileNotFoundError, json.JSONDecodeError):
          print('There are no cards within the deck. Please add them.')
          mode_search()

     counter = 1
     while counter > 0:
          again = input('''\n Would you like to check if deck is legal?
          click 1 as yes 
          click 2 as no
          : ''')

          if again == '1':
               print('Your deck being legal is', deck_legal)
               match reason:
                    case 'too many of card':
                         for card, count in card_counts.items():
                              if count > 3:
                                   print(f'{card}', 'in deck more than three time please go down to limit')
                    case 'too many in total':
                         print('There are too many cards in your deck, not proper for use')
                    case 'too little in total':
                         print('There are too little cards in your deck for it to be legal')
                    case 'card number in main invalid':
                         print('Number of cards in main deck is invalid')
                    case 'card number in extra invalid':
                         print('Number of cards in extra deck is invalid')
          elif again == '2':
               counter = 0
          else:
               print('incorrect response')


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

#ERROR FUNCTION MAPPED TO VALIDATION
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
          
#FUNCTION TO SANITISE SEARCHES INTO API
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

# MODE CODES TO RUN WHEN MODES CHANGE
def mode_open(username):
     global deck_name
     user_folder = os.path.join(os.getcwd(), username)
     if not os.path.exists(user_folder):
          print(f"User folder '{username}' does not exist.Deck creation not possible")
          mode_changer()
     
     deck_name = input('What is the name of the deck you would like to open?: ')

     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     if not os.path.exists(deck_file_path):
          print('deck does not exist please create it')
          mode_create(username)
     else:
          mode_search()

def mode_stop():
     quit()

def mode_dbe(call_return,username,deck_name):
     #print('Mode was changed')
     inital_search_func(call_return)
     counter_for_cards = 1
     while counter_for_cards > 0:
          again = input('''Would you like to add the cards searched or delete the last card added?
          click 1 to add
          click 2 to delete
          : ''')

          if again == '1':
               save_card_to_deck(call_return,username,deck_name)
               counter_for_cards = 0
          elif again == '2':
               card_name_to_remove = input('What is the exact name of the card you want to remove: ')
               delete_card_from_deck(username,deck_name,card_name_to_remove)
               counter_for_cards = 0
          else:
               print('incorrect response')
     deck_check(username,deck_name)
     #on_click_search_func(call_return)
     # add = save_card_to_deck(deckname, username, call_return)

     # if add == False:
     #      mode = 'create'

     counter_for_modes = 1
     while counter_for_modes > 0:
          again = input('''Would you like to search again?
          click 1 to search again 
          click 2 to stop
          : ''')

          if again == '1':
               mode_search()
               counter_for_modes = 0
          elif again == '2':
               mode_stop()
               counter_for_modes = 0
          else:
               print('incorrect response')

def mode_create(username):
     global deck_name
     deck_name = input('what is the name of your deck: ')

     user_folder = os.path.join(os.getcwd(), username)

     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     if os.path.exists(deck_file_path):
        print(f"Deck '{deck_name}' already exists.")
        mode_create(username)
     else:
          create_deck_file(deck_name,username)
          mode_search()

def mode_search():
     search_dict = {}
     parameter_number = input('how many parameters would you like to pass?: ')
     while not parameter_number.isdigit():
               print('Error input was not a number')
               parameter_number = input('how many parameters would you like to pass?: ')

     parameter_number = int(parameter_number)

     while parameter_number > 15 :
          print('Too many parameters retry')
          while not parameter_number.isdigit():
               print('Error input was not a number')
               parameter_number = input('how many parameters would you like to pass?: ')

     parameter_number = int(parameter_number)

     for i in range(parameter_number):
          Flag = False
          while Flag == False:
               card_parameter = input('Param: ') # takes in parameter for search
               corresponding_variable = input('Variable: ') # the variable correspoding to the parameter that the user wants to actually search for like a specific card type or card.
               if card_parser_validator(card_parameter,corresponding_variable):
                    search_dict[card_parameter] = corresponding_variable
                    break
               else:
                    print('Invalid parameter please try again')

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
               mode_dbe(call_return,username,deck_name)
               counter = 0
          elif again == '3':
               mode_stop()
               counter = 0
          else:
               print('incorrect response')

#FUNCTION THAT CHANGES MODES
def mode_changer():
     counter = 1
     while counter > 0 :
          print('The list of possible modes are',f'{list_of_modes}')
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
                    case 'open':
                         mode_open(username)
     
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
               mode_changer()
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
