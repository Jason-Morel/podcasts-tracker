# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:45:28 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
#from colorama import Fore, Back, Style
from send_message import send_telegram_message



###You might see some comments as the 4 lines below.
# #User inputs:
# input_key_words = 'économie'
# input_duration =  '15 to 30'
# time_choice = 2
###These comments are pieces of code which have been useful during the development process.
###They are kept as comments along this file to make debugging easier.



#Authentication - without user.
#This step is to 'log' in the Spotify API.
#Remark: 
    #It is not good practice to share API's credentials on GitHub.
    #These keys should remain secret. Otherwise, anyone on GitHub could use the API with your account.
    #You don't want this to happen. Especially if you registered your credit card details on the API...
#Here we share our API's credentials because Spotify API is free to use. So we don't risk to be hacked.
#Sharing our credentials makes our program easy to use for everyone.
def authenticate():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                             client_secret='90eb460ff94847998926f6d380532f59'))
    return sp



#Find shows related to the input keyword.
#French market is set by default.
def get_shows(key_words, input_offset):
    shows = sp.search(q=key_words, limit=50, offset=input_offset, type='show', market='fr')
    return shows
    #for idx, show in enumerate(shows['shows']['items']):
        #print(show['publisher'], ':', show['name'], show['languages'], show['id'])



#Remove shows which are not matching selected language.
#As of now, french is set by default.
#But this function makes it easy to set language as an input.
def remove_other_languages():
    for idx, show in enumerate(shows['shows']['items']):
        shows['shows']['items'][idx]['languages'] = str(shows['shows']['items'][idx]['languages']).lower()
        if re.search('fr', shows['shows']['items'][idx]['languages']) == None:
            #print(shows['shows']['items'][idx]['name'], shows['shows']['items'][idx]['languages'])
            del shows['shows']['items'][idx]
    return shows



#/!\ WARNING /!\
#I have noticed that remove_other_languages doesn't work when input_key_word = 'donut'.
#I am guessing it has something to do with the fact that donut isn't a french word per se.
#But the function re.search should still delete any show for which 'languages' is not matching 'fr'.
#So the problem might come from this re.search actually.
#To run an example of this bug, please see 'donut_issue.py' in this repo.



##The result object from function sp.search doesn't contain any information about shows' duration.
##It makes sense because shows are composed by several episodes of different durations.
##Therefore the idea behind the following lines is to approximate a shows 'duration' from its episodes durations.

#1-Add a new key (called 'episodes') to the shows['shows']['items'][idx] dictionaries. 
#It's a dictionary which contains descriptions of the show's first 50 episodes.
def get_episodes():
    for idx, show in enumerate(shows['shows']['items']):
        shows['shows']['items'][idx]['episodes'] = sp.show_episodes(show_id=shows['shows']['items'][idx]['id'], limit=50, market='fr')
    return shows
        


#2-Add a new key (called 'duration_ms') to the shows['shows']['items'][idx] dictionaries. 
#It's a list which contains durations (in ms) of the show's first 50 episodes. 
def get_durations():
    for idx, show in enumerate(shows['shows']['items']):
        duration_ms = []
        for i, episode in enumerate(shows['shows']['items'][idx]['episodes']['items']):
            duration_ms.append(shows['shows']['items'][idx]['episodes']['items'][i]['duration_ms'])
            shows['shows']['items'][idx]['durations_ms'] = duration_ms
    return shows


    
#3-Find min and max values of the duration_ms list
def get_min_max():
    #3.1-Convert lists into Pandas DataFrames
    for idx, show in enumerate(shows['shows']['items']):
        shows['shows']['items'][idx]['durations_ms'] = pd.DataFrame({'duration_ms':shows['shows']['items'][idx]['durations_ms']})

    #3.2-Add a new key (called 'min_max') to the shows['shows']['items'][idx] dictionaries. 
    #It's a dictionary which contains the min (10th percentile) and max (90th percentile) of the show's first 50 episodes. 
    for idx, show in enumerate(shows['shows']['items']):
        durations_ms = shows['shows']['items'][idx]['durations_ms']
        #Convert min and max into minutes:
        shows['shows']['items'][idx]['min_max'] = {'min':round(int(durations_ms.quantile(q=0.1))/60000,2), 
                                                   'max':round(int(durations_ms.quantile(q=0.9))/60000,2)}
    return shows



# #To have an idea of the intervals we can expect with this method:
# for idx, show in enumerate(shows['shows']['items']):
#     print(shows['shows']['items'][idx]['min_max'])


    
#Drop shows for which episode duration is not regular enough
#Shows for which max-min > 15 minutes will be droped.
def keep_shows_with_regular_duration():  
    for idx, show in enumerate(shows['shows']['items']):
        if shows['shows']['items'][idx]['min_max']['min']<45:
            if shows['shows']['items'][idx]['min_max']['max']-shows['shows']['items'][idx]['min_max']['min']>15:
                #print(shows['shows']['items'][idx]['min_max'])
                del shows['shows']['items'][idx]
    return shows



##Assign a duration span to each show

#1-Round min and max to get clean duration spans
def round_min_max():
    for idx, show in enumerate(shows['shows']['items']):
        if shows['shows']['items'][idx]['min_max']['min']>5:
            shows['shows']['items'][idx]['min_max']['min'] = int(round(shows['shows']['items'][idx]['min_max']['min']
                                                                       -shows['shows']['items'][idx]['min_max']['min']%5, 0))
            shows['shows']['items'][idx]['min_max']['max'] = int(round(shows['shows']['items'][idx]['min_max']['max']
                                                                       -shows['shows']['items'][idx]['min_max']['max']%5, 0))
    
    for idx, show in enumerate(shows['shows']['items']):
        if shows['shows']['items'][idx]['min_max']['min']<5 and shows['shows']['items'][idx]['min_max']['max']<6:
            shows['shows']['items'][idx]['min_max']['min'] = 0
            shows['shows']['items'][idx]['min_max']['max'] = 5
    
    for idx, show in enumerate(shows['shows']['items']):
        if shows['shows']['items'][idx]['min_max']['min']<5 and shows['shows']['items'][idx]['min_max']['max']>6:
            shows['shows']['items'][idx]['min_max']['min'] = 5
            shows['shows']['items'][idx]['min_max']['max'] = int(round(shows['shows']['items'][idx]['min_max']['max']
                                                                       +5
                                                                       -shows['shows']['items'][idx]['min_max']['max']%5, 0))
    return shows



#2-Create uniform duration spans
def get_uniform_duration_spans():
    for idx, show in enumerate(shows['shows']['items']):
        if shows['shows']['items'][idx]['min_max']['min'] == 0 and shows['shows']['items'][idx]['min_max']['max'] == 5:
            shows['shows']['items'][idx]['duration_span'] = 'under 5'
        if 5 <= shows['shows']['items'][idx]['min_max']['min'] <= 15 and 5 <= shows['shows']['items'][idx]['min_max']['max'] <= 15:
            shows['shows']['items'][idx]['duration_span'] = '5 to 15'
        if 5 <= shows['shows']['items'][idx]['min_max']['min'] <= 15 and 15 <= shows['shows']['items'][idx]['min_max']['max'] <= 30:
            shows['shows']['items'][idx]['duration_span'] = '15 to 30'
        if 15 <= shows['shows']['items'][idx]['min_max']['min'] <= 30 and 15 <= shows['shows']['items'][idx]['min_max']['max'] <= 30:
            shows['shows']['items'][idx]['duration_span'] = '15 to 30'
        if 15 <= shows['shows']['items'][idx]['min_max']['min'] <= 30 and 30 <= shows['shows']['items'][idx]['min_max']['max'] <= 45:
            shows['shows']['items'][idx]['duration_span'] = '30 to 45'
        if 30 <= shows['shows']['items'][idx]['min_max']['min'] <= 45 and 30 <= shows['shows']['items'][idx]['min_max']['max'] <= 45:
            shows['shows']['items'][idx]['duration_span'] = '30 to 45'
        if 30 <= shows['shows']['items'][idx]['min_max']['min'] <= 45 and 45 <= shows['shows']['items'][idx]['min_max']['max']:
            shows['shows']['items'][idx]['duration_span'] = 'over 45'
        if 45 <= shows['shows']['items'][idx]['min_max']['min']:
            shows['shows']['items'][idx]['duration_span'] = 'over 45'
    return shows



# #Check that every shows are assigned to a span
# for idx, show in enumerate(shows['shows']['items']):
#     try:
#         print(Fore.GREEN+ shows['shows']['items'][idx]['name'], shows['shows']['items'][idx]['duration_span'])
#     except KeyError:
#         print(Fore.RED + 'span does not exist', idx)


#The following function has been created for the sake of compatibility between show_treatment and episode_treatment
def range_for_shows(time_choice):
    if time_choice == 1:
        input_duration = 'under 5'
        return input_duration
    elif time_choice == 2:
        input_duration = '5 to 15'
        return input_duration
    elif time_choice == 3:
        input_duration = '15 to 30'
        return input_duration
    elif time_choice == 4:
        input_duration = '30 to 45'
        return input_duration
    elif time_choice == 5:
        input_duration = 'over 45'
        return input_duration    



##Return shows which are matching input_duration
def return_shows(span, chat_id, TOKEN_telegram):
    ready_to_send = {}
    send_telegram_message("Voici une liste de plusieurs émissions correspondant à votre recherche :", chat_id, TOKEN_telegram)
    for idx, show in enumerate(shows['shows']['items']):
        try:
            if shows['shows']['items'][idx]['duration_span'] == span:
                #print(Fore.CYAN + show['name'], Fore.MAGENTA + show['duration_span'])
                send_telegram_message(f"{show['name']}\n{show['external_urls']['spotify']}", chat_id, TOKEN_telegram)
                ready_to_send[idx] = shows['shows']['items'][idx] #This dictionary will allow us to count how many results have been sent.
        except KeyError:
            del shows['shows']['items'][idx] 
    return ready_to_send

#except KeyError has been added below in case a show is not assigned to any span.
#It will delete the 'lost' show and the loop will keep going instead of getting a KeyError.



def find_shows(input_key_words, time_choice, chat_id, TOKEN_telegram):
    
    start_offset = 0
    sent = 0

    global sp
    global shows

    
    sp = authenticate()
    input_duration = range_for_shows(time_choice)


    while sent < 5:
        shows = get_shows(input_key_words, start_offset)
        start_offset += 50
        shows = remove_other_languages()
        shows = get_episodes()
        shows = get_durations()
        shows = get_min_max()
        shows = keep_shows_with_regular_duration()
        shows = round_min_max()
        shows = get_uniform_duration_spans()
        ready_to_send = return_shows(input_duration, chat_id, TOKEN_telegram)
        sent += len(ready_to_send)

#Function sp.search gives at most 50 results. It means we have to launch another search if we want more than 50 results.
#That's what the start_offset is for. It allows us to get the next 50 results instead of getting the same results as the first search.

    

#Some ways to improve our tool (non-exhaustive):
    #If there isn't any result with a pair (keyword; duration), we could ask if user wants to see results for other durations (if there are any).
    #OR the user could be asked only a subject and algo could send results which are grouped by duration.      