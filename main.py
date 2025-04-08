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

#GUI intializing CODE


dpg.create_context()
dpg.configure_app(docking=True, docking_space=True, load_init_file="custom_layout.ini")
dpg.create_viewport()


def hide_window(name):
     if dpg.does_item_exist(name):
          #print(name)
          dpg.hide_item(name)
     # else:
     #      error('window')

def delete_window(name):
     if dpg.does_item_exist(name):
          #print(name)
          dpg.delete_item(name)
     # else:
     #      error('window')

def show_window(name):
     if dpg.does_item_exist(name):
          #print(name)
          dpg.show_item(name)
     # else:
     #      error('window')

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
     search_data =json.loads(j_compact_print(search.json()))

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

                    with dpg.window(label='Search result',tag='search_result'):
                         dpg.add_text('your search result is')
                         dpg.add_text(f'{inital_search_func(r)}',multiline=True)
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
               case 'window':
                    print('The window you have called does not exist')
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


def mode_open_GUI():
     if dpg.does_item_exist('mode_choose'):
          delete_window('mode_choose')
     with dpg.window(label='Opening deck',tag='open_deck'):
          dpg.add_text('please delete and ignore the other window library side error')
          dpg.add_input_text(label='enter deck name:',tag='deck_name')
          dpg.add_button(label='enter',tag='enter_open',callback=mode_open,user_data=username)

def mode_open(sender,app_data,user_data):
     global deck_name
     user_folder = os.path.join(os.getcwd(), user_data)
     if not os.path.exists(user_folder):
          print(f"User folder '{user_data}' does not exist. Deck creation not possible")

     deck_name = dpg.get_value('deck_name')

     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     if not os.path.exists(deck_file_path):
          with dpg.window(label='Deck does not exist',tag='deck_unreal'):
               dpg.add_text('deck does not exist please create it')
               time.sleep(1)
               mode_create_GUI()
               delete_window('deck_unreal')
     else:
          with dpg.window(label='Deck opened',tag='open_success'):
               dpg.add_text('deck opened successfully')
               time.sleep(1)
               delete_window('open_success')
          mode_search_GUI(0)

def mode_stop(sender):
     quit()

def mode_dbe(call_return,username,deck_name):
     #print('Mode was changed')
     on_click_search_func(call_return)
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

def mode_create_GUI():
     if dpg.does_item_exist('mode_choose'):
          delete_window('mode_choose')
     if dpg.does_item_exist('open_deck'):
          delete_window('open_deck')
     with dpg.window(label='deck creation',tag='deck_create'):
          dpg.add_text('please delete and ignore the other window library side error')
          dpg.add_input_text(label='enter deck name: ',tag='deck_name')
          dpg.add_button(label='enter',tag='enter_create',callback=mode_create,user_data=username)


def mode_create(sender,app_data,user_data):
     global deck_name
     deck_name = dpg.get_value('deck_name')

     user_folder = os.path.join(os.getcwd(),user_data)

     deck_file_path = os.path.join(user_folder, f"{deck_name}.json")
     if os.path.exists(deck_file_path):
        with dpg.window(label='Deck with that name exists',tag='deck_isrealalr'):
             dpg.add_text(f"Deck '{deck_name}' already exists. Please try again")
             time.sleep(1)
             delete_window('deck_isrealalr')
     else:
          with dpg.window(label='Deck made',tag='create_success'):
               dpg.add_text('deck made successfully')
               time.sleep(1)
               delete_window('create_success')
          create_deck_file(deck_name,user_data)
          mode_search()


def mode_search_GUI(sender):
     if dpg.does_item_exist('deck_create'):
          delete_window('deck_create')
     if dpg.does_item_exist('open_deck'):
          delete_window('open_deck')

     with dpg.item_handler_registry(tag='click_check') as handler:
          dpg.add_item_clicked_handler(callback=mode_search_click_check)
     with dpg.item_handler_registry(tag='visble_check') as handler:
          dpg.add_item_visible_handler(callback=mode_search_visble_check)

     with dpg.window(label='Getting param number',tag='param_num_ask',width=1920,height=1080):
          dpg.add_input_text(label='how many parameters would you like to pass?:',tag='parameter_number')
          dpg.add_button(label='enter',tag='enter_search')
          dpg.add_button(label='dummy button',tag='dummy',show=False)

     dpg.bind_item_handler_registry('enter_search','click_check')
     dpg.bind_item_handler_registry('dummy','visble_check')

def mode_search_click_check(sender):
     global parameter_number
     parameter_number = str(dpg.get_value('parameter_number'))
     while not parameter_number.isdigit():
               with dpg.window(label='Input error',tag='input_error'):
                    dpg.add_text('Error input was not a number')
                    time.sleep(1)
                    delete_window('input_error')

     parameter_number = int(parameter_number)
     
     while parameter_number > 15 :
          with dpg.window(label='Input error',tag='input_error2'):
                    dpg.add_text('Error input number greater 15')
                    time.sleep(1)
                    delete_window('input_error2')
          while not parameter_number.isdigit():
               with dpg.window(label='Input error',tag='input_error'):
                    dpg.add_text('Error input was not a number')
                    time.sleep(1)
                    delete_window('input_error')

     if parameter_number <= 15:          
          dpg.hide_item('parameter_number')
          dpg.hide_item('enter_search')
          dpg.show_item('dummy')


def mode_search_visble_check(sender):
     delete_window('param_num_ask')
     with dpg.window(label='Taking in data',tag='search_data',width=1920,height=1080):
          dpg.add_text('Please input card parameters and corresponding variables (to add new ones remove old and click enter again)')
          dpg.add_text(f'The parameters passable are name,fname,id,type,atk,def,level,race,attribute,link,linkmarker,scale,cardset,archetype,banlist')
          dpg.add_input_text(label='Parameter: ',tag='card_parameter')
          dpg.add_input_text(label='Variable:',tag='corresponding_variable')
          dpg.add_button(label='enter',tag='enter_search',callback=mode_search,user_data=parameter_number)

# def mode_search_parameter_num(sender):
#      parameter_number = str(dpg.get_value('parameter_number'))
#      while not parameter_number.isdigit():
#                with dpg.window(label='Input error',tag='input_error'):
#                     dpg.add_text('Error input was not a number')
#                     time.sleep(1)
#                     delete_window('input_error')

#      parameter_number = int(parameter_number)
     
#      while parameter_number > 15 :
#           with dpg.window(label='Input error',tag='input_error2'):
#                     dpg.add_text('Error input number greater 15')
#                     time.sleep(1)
#                     delete_window('input_error2')
#           while not parameter_number.isdigit():
#                with dpg.window(label='Input error',tag='input_error'):
#                     dpg.add_text('Error input was not a number')
#                     time.sleep(1)
#                     delete_window('input_error')


     

def mode_search(sender,app_data,user_data):
     search_dict = {}
     
     parameter_number = user_data

     for i in range(parameter_number):
          Flag = False
          while Flag == False:
               card_parameter = str(dpg.get_value('card_parameter'))# takes in parameter for search
               corresponding_variable = str(dpg.get_value('corresponding_variable'))# the variable correspoding to the parameter that the user wants to actually search for like a specific card type or card.
               if card_parser_validator(card_parameter,corresponding_variable):
                    search_dict[card_parameter] = corresponding_variable
                    break
               else:
                    with dpg.window(label='Invalid param',tag='invalid_param'):
                         dpg.add_text('Parameter was invalid please retry')
                         time.sleep(1)
                         delete_window('invalid_param')

     if search_dict:
          call_return = database_call(search_dict)
     else:
          with dpg.window(label='Invalid param',tag='invalid_param2'):
                         dpg.add_text('Parameter was invalid please retry')
                         time.sleep(1)
                         delete_window('invalid_param2')


     counter = 1
     while counter > 0:
          with dpg.window(label='post result',tag='post_result'):
               dpg.add_text('search complete access deck builder or search again or close program?')
               dpg.add_button(label='search again',tag='search_again',callback=mode_create_GUI)
               dpg.add_button(label='begin deck build',tag='deck_build',callback=mode_dbe_GUI,)
               dpg.add_button(label='close program',tag='stop',callback=mode_stop)
               counter = 0
#FUNCTION THAT CHANGES MODES

def mode_changer(sender,app_data,user_data):
     counter = 1
     while counter > 0 :
          #print(user_data)
          if user_data not in list_of_modes:
               print('incorrect mode')
          else:
               match user_data:
                    case 'search':
                         mode_search()
                    case 'dbe':
                         mode_dbe()
                    case 'stop':
                         mode_stop()
                    case 'create':
                         mode_create_GUI()
                    case 'open':
                         mode_open_GUI()

def mode_order():
     delete_window('account_login')
     with dpg.window(label='mode chosse',tag='mode_choose'):
          dpg.add_text('Would you like to create a deck or open one?')
          dpg.add_button(label='create',tag='deck_create',callback=mode_changer,user_data='create')
          dpg.add_button(label='open',tag='deck_open',callback=mode_changer,user_data='open')
     
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

def login_GUI(sender):
     if dpg.does_item_exist(entry_window) ==  True:
          delete_window(entry_window)
     if dpg.does_item_exist('account_create'):
          delete_window('account_create')

     with dpg.window(label='Login',tag='account_login',width=1920,height=1080):
          dpg.add_input_text(label='Username: ',tag='username')
          dpg.add_input_text(label='Password: ',tag='password')
          dpg.add_button(label='Enter',callback=login)

def login():
     counter = 1
     while counter > 0:
          global username
          global password
          username = str(dpg.get_value('username'))
          password = str(dpg.get_value('password'))
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
               with dpg.window(label='Log in successful',tag='login_success'):
                    dpg.add_text('Logged in successfully')
                    time.sleep(1)
                    delete_window('account_login')
                    delete_window('login_success')
                    mode_order()
          else:
               counter= 0
               with dpg.window(label='Login fail',tag='login_fail'):
                    dpg.add_text('Log in failed please try again or create an account')
                    dpg.add_button(label='Create',callback=create_accounts_GUI)
                    time.sleep(1)
                    delete_window('login_fail')

          

#reads the existing accounts and creates a new account based on that
def create_accounts_GUI(sender):
     with dpg.window(label='Create',tag='account_create',width=1920,height=1080):
          delete_window(entry_window)
          dpg.add_input_text(label='Username: ',tag='username')
          dpg.add_input_text(label='Password: ',tag='password')
          dpg.add_button(label='Enter',callback=create_accounts)

def create_accounts():
     counter = 1
     while counter > 0:
          create_username = str(dpg.get_value('username'))
          create_password = str(dpg.get_value('password'))
          username_exists = False
          logins = read_accounts()
          for line in logins:
               if line[0] == create_username:
                    username_exists = True
                    break
          if username_exists:
               with dpg.window(label='Creation fail',tag='create_fail'):
                    counter = 0
                    dpg.add_text('Creation failed username already exists please try again')
                    time.sleep(1)
                    delete_window('create_fail')
          else:
               with open('Accounts_NEA.txt', 'a') as account_make:
                    account_make.write(f'{create_username},{create_password}\n')

               with dpg.window(label='Creation successful',tag='create_success'):
                    dpg.add_text('Account created successfully')
                    time.sleep(1)
                    delete_window('create_success')
               print('Account created successfully')

               user_folder = os.path.join(os.getcwd(), create_username)
               if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                    print(f'Folder "{create_username}" created successfully.')
               else:
                    print(f'Folder "{create_username}" already exists.')
                         
               counter = -1
               delete_window('account_create')
               login_GUI(0)

#GUI CODE START

entry_window = 1

with dpg.window(label='Entrypage',tag=entry_window,width=1920,height=1080):
     dpg.add_text('Welcome to the yugioh duel matrix, please login or create an account')
     dpg.add_button(label='Login',callback=login_GUI)
     dpg.add_button(label='Create',callback=create_accounts_GUI)




dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()



#terminal side UI for test

# check = False
# while check == False :
#      entry = input('''Welcome to the program:
#                click 1 to create an account
#                click 2 to login
#                : ''')
#      if entry == '1':
#           create_accounts()
#           check = True
#      elif entry == '2':
#           login()
#           check = True
