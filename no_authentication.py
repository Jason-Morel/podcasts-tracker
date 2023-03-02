# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:45:28 2023

@author: Jason
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
from colorama import Fore, Back, Style



#Authentication - without user
def authenticate():
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="CLIENT_ID",
                                                               client_secret="CLIENT_SECRET"))
    return sp

sp = authenticate()



#User inputs
input_language = 'fr'
input_key_words = 'arbre'
input_duration =  '5 to 15'



#Find shows related to economy in French market
def get_shows(key_words, language):
    shows = sp.search(q=key_words, limit=50, type='show', market=language)
    return shows
    #for idx, show in enumerate(shows['shows']['items']):
        #print(show['publisher'], ':', show['name'], show['languages'], show['id'])

shows = get_shows(key_words=input_key_words, language=input_language)



#Find the next 50 shows related to economy in French market (if none of the first 50 episodes matches the expected duration)
shows_50 = sp.search(q='économie', limit=50, offset=50, type='show', market='FR')
for idx, show in enumerate(shows_50['shows']['items']):
    print(show['publisher'], ':', show['name'], show['languages'], show['id'])

###TO DO: 
    #create a loop to search for more shows if there isn't enough results with the first 50 shows.
    #add these additional results on top of the first dictionary.



##Remove shows which are not matching selected language (LYNA: allow user to select languages)
def remove_other_languages(language):
    for idx, show in enumerate(shows['shows']['items']):
        shows['shows']['items'][idx]['languages'] = str(shows['shows']['items'][idx]['languages']).lower()
        if re.search(language, shows['shows']['items'][idx]['languages']) == None:
            print(shows['shows']['items'][idx]['name'], shows['shows']['items'][idx]['languages'])
            del shows['shows']['items'][idx]
    return shows

shows = remove_other_languages(language=input_language)

#/!\ WARNING /!\
#I have noticed that remove_other_languages doesn't work when input_key_word = 'donut'.
#I am guessing it has something to do with the fact that donut isn't a french word per se.
#To run an example of this bug, please see 'donut_issue.py' in this repo.



##Look at the distribution of the variable duration_ms for the set of episodes
#1-Add a new key (called 'episodes') to the shows['shows']['items'][idx] dictionaries. It's a dictionary which contains descriptions of the show's first 50 episodes.
for idx, show in enumerate(shows['shows']['items']):
    shows['shows']['items'][idx]['episodes'] = sp.show_episodes(show_id=shows['shows']['items'][idx]['id'], limit=50, market='FR')

#2-Add a new key (called 'duration_ms') to the shows['shows']['items'][idx] dictionaries. It's a list which contains durations (in ms) of the show's first 50 episodes. 
for idx, show in enumerate(shows['shows']['items']):
    duration_ms = []
    for i, episode in enumerate(shows['shows']['items'][idx]['episodes']['items']):
        duration_ms.append(shows['shows']['items'][idx]['episodes']['items'][i]['duration_ms'])
        shows['shows']['items'][idx]['durations_ms'] = duration_ms
    
#3-Find min and max values of the duration_ms list
#3.1-Convert lists into Pandas DataFrames
for idx, show in enumerate(shows['shows']['items']):
    shows['shows']['items'][idx]['durations_ms'] = pd.DataFrame({'duration_ms':shows['shows']['items'][idx]['durations_ms']})
#Add a new key (called 'min_max') to the shows['shows']['items'][idx] dictionaries. It's a dictionary which contains the min (10th percentile) and max (90th percentile) of the show's first 50 episodes. 
for idx, show in enumerate(shows['shows']['items']):
    durations_ms = shows['shows']['items'][idx]['durations_ms']
    shows['shows']['items'][idx]['min_max'] = {'min':round(int(durations_ms.quantile(q=0.1))/60000,2), 'max':round(int(durations_ms.quantile(q=0.9))/60000,2)} #min and max are converted to minutes

#To have an idea of the intervals we can expect with this method:
for idx, show in enumerate(shows['shows']['items']):
    print(shows['shows']['items'][idx]['min_max'])
    
#Drop shows for which episode duration is not regular enough    
for idx, show in enumerate(shows['shows']['items']):
    if shows['shows']['items'][idx]['min_max']['min']<45:
        if shows['shows']['items'][idx]['min_max']['max']-shows['shows']['items'][idx]['min_max']['min']>15:
            #print(shows['shows']['items'][idx]['min_max'])
            del shows['shows']['items'][idx]

##Assign a duration span to each show
#Round min and max to get clean duration spans
for idx, show in enumerate(shows['shows']['items']):
    if shows['shows']['items'][idx]['min_max']['min']>5:
        shows['shows']['items'][idx]['min_max']['min'] = int(round(shows['shows']['items'][idx]['min_max']['min'] - shows['shows']['items'][idx]['min_max']['min']%5, 0))
        shows['shows']['items'][idx]['min_max']['max'] = int(round(shows['shows']['items'][idx]['min_max']['max'] - (shows['shows']['items'][idx]['min_max']['max']%5), 0))

for idx, show in enumerate(shows['shows']['items']):
    if shows['shows']['items'][idx]['min_max']['min']<5 and shows['shows']['items'][idx]['min_max']['max']<6:
        shows['shows']['items'][idx]['min_max']['min'] = 0
        shows['shows']['items'][idx]['min_max']['max'] = 5

for idx, show in enumerate(shows['shows']['items']):
    if shows['shows']['items'][idx]['min_max']['min']<5 and shows['shows']['items'][idx]['min_max']['max']>6:
        shows['shows']['items'][idx]['min_max']['min'] = 5
        shows['shows']['items'][idx]['min_max']['max'] = int(round(shows['shows']['items'][idx]['min_max']['max'] + 5-(shows['shows']['items'][idx]['min_max']['max']%5), 0))
        
#Create uniform duration spans
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

#Check that all every shows are assigned to a span
for idx, show in enumerate(shows['shows']['items']):
    try:
        print(Fore.GREEN+ shows['shows']['items'][idx]['name'], shows['shows']['items'][idx]['duration_span'])
    except KeyError:
        print(Fore.RED + 'span does not exist')
        
##Filter shows by duration
for idx, show in enumerate(shows['shows']['items']):
    if shows['shows']['items'][idx]['duration_span'] == '5 to 15':
        print(Fore.CYAN + show['name'], Fore.MAGENTA + show['duration_span'])



#If there isn't any result with a pair (subject; duration), we could ask if user wants to see results for other durations (if there is any).
#OR the user could be asked only a subject and algo could send results which are grouped by duration.      


#Because people usually commute twice a day (home -> office AND office -> home): we could return episodes matching the duration selected by user AND episodes which are twice as long.
#It would allow the user to listen half of the episode in the morning and the other half in the evening.

#How can we approximate episodes duration if API limits the results to 50?
#We could look at the distribution of episodes duration for a specific show.
#Then we would recommend shows to user (instead of episodes).
#It means our tool would not need to be used everyday. Instead, user could use our tool when they feel like discovering new shows which match a specific topic.