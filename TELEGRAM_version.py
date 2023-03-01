#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:41:17 2023

@author: lyna
"""

# S'assurer d'avoir fait "%reset" dans la console au début

import spotipy # la librairie pour manipuler l'api spotify
import spotipy.util as util
import requests
import re
import time
import pandas as pd
from colorama import Fore, Back, Style


# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather
chat_id = "5561504638" #obtenu en allant sur https://api.telegram.org/bot{TOKEN_telegram}/getUpdates

# AUTHENTIFICATION spotipy
username="31aon4o2j7wikppjnfxfvpvptjtu?si=442993df78a74794"
clientId= "e48f42372a074a25b7a0d25da48439d6"
clientSecret="90eb460ff94847998926f6d380532f59"
 
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username,scope,client_id=clientId,client_secret=clientSecret,redirect_uri='https://github.com/Jason-Morel/podcasts-tracker')
if token:
     sp = spotipy.Spotify(auth=token)
     sp.trace = False
     

# fonction pour envoyer un message à Telegram
def send_telegram_message(message): # demander à Jason pour fonction propre
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    

    # Demande du temps d'écoute souhaité
    
# envoyer les messages à Telegram
send_telegram_message("Quel est le temps d'écoute que vous souhaitez ?\n1. Moins de 5 minutes\n2. De 5 à 15 minutes\n3. De 15 à 30 minutes\n4. De 30 à 45 minutes\n5. Plus de 45 minutes")
send_telegram_message("Entrez le numéro correspondant à votre choix : ")

time.sleep(10)

# récupérer la réponse de l'utilisateur
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates") 
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
time_choice = int(text)

if time_choice == 1:
    time_choice = 'under 5'
elif time_choice == 2:
    time_choice = '5 to 15'
elif time_choice == 3:
    time_choice = '15 to 30'
elif time_choice == 4:
    time_choice = '30 to 45'
elif time_choice == 5:
    time_choice = 'over 45'
    
if time_choice == 1:
   min_duration = 0
   max_duration = 600000
elif time_choice == 2:
   min_duration = 600000
   max_duration = 1200000
elif time_choice == 3:
   min_duration = 1200000
   max_duration = 1800000
elif time_choice == 4:
   min_duration = 1800000
   max_duration = 2400000
elif time_choice == 5:
   min_duration = 2400000
   max_duration = 3000000
elif time_choice == 6:
   min_duration = 3000000
   max_duration = 3600000
elif time_choice == 7:
   min_duration = 3600000
   max_duration = 10**1000


# Demande de la langue d'écoute
send_telegram_message("Quelle langue souhaitez-vous pour vos podcasts ?\n\nVoici les différents codes : Français=fr, Allemand=de, Anglais=en, Espagnol=es, Italien=it")
send_telegram_message("Entrez le code correspondant à votre choix : ")


time.sleep(20)

# Récupérer la ou les langue(s) entrée(s) sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
language = str(text)


# Demande de mot clé à l'utilisateur
send_telegram_message("Quel type de podcast souhaitez-vous écouter aujourd'hui ?\nEntrez le thème de votre choix : ")
   
time.sleep(15)

# Récupérer le mot exact entré sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
search_word = str(text)
search_word = re.sub(r' ', '', search_word)


################################ PARTIE SHOW ########################################
# Implémentation du mot exact dans la fonction search
shows_0 = sp.search(q=f'{search_word}', limit=50, type='show', market='FR')

# Supprimer les show qui ne sont pas de la langue choisie
languages = f'{language}'
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['languages'] = str(shows_0['shows']['items'][idx]['languages']).lower()
    if re.search(languages, shows_0['shows']['items'][idx]['languages']) == None:
        del shows_0['shows']['items'][idx]


#1-Add a new key (called 'episodes') to the shows_0['shows']['items'][idx] dictionaries. It's a dictionary which contains descriptions of the show's first 50 episodes.
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['episodes'] = sp.show_episodes(show_id=shows_0['shows']['items'][idx]['id'], limit=50, market='FR')

#2-Add a new key (called 'duration_ms') to the shows_0['shows']['items'][idx] dictionaries. It's a list which contains durations (in ms) of the show's first 50 episodes. 
for idx, show in enumerate(shows_0['shows']['items']):
    duration_ms = []
    for i, episode in enumerate(shows_0['shows']['items'][idx]['episodes']['items']):
        duration_ms.append(shows_0['shows']['items'][idx]['episodes']['items'][i]['duration_ms'])
        shows_0['shows']['items'][idx]['durations_ms'] = duration_ms
    
#3-Find min and max values of the duration_ms list
#3.1-Convert lists into Pandas DataFrames
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['durations_ms'] = pd.DataFrame({'duration_ms':shows_0['shows']['items'][idx]['durations_ms']})
#Add a new key (called 'min_max') to the shows_0['shows']['items'][idx] dictionaries. It's a dictionary which contains the min (10th percentile) and max (90th percentile) of the show's first 50 episodes. 
for idx, show in enumerate(shows_0['shows']['items']):
    durations_ms = shows_0['shows']['items'][idx]['durations_ms']
    shows_0['shows']['items'][idx]['min_max'] = {'min':round(int(durations_ms.quantile(q=0.1))/60000,2), 'max':round(int(durations_ms.quantile(q=0.9))/60000,2)} #min and max are converted to minutes
    
#Drop shows for which episode duration is not regular enough    
for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['min_max']['min']<45:
        if shows_0['shows']['items'][idx]['min_max']['max']-shows_0['shows']['items'][idx]['min_max']['min']>15:
            #print(shows_0['shows']['items'][idx]['min_max'])
            del shows_0['shows']['items'][idx]

##Assign a duration span to each show
#Round min and max to get clean duration spans
for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['min_max']['min']>5:
        shows_0['shows']['items'][idx]['min_max']['min'] = int(round(shows_0['shows']['items'][idx]['min_max']['min'] - shows_0['shows']['items'][idx]['min_max']['min']%5, 0))
        shows_0['shows']['items'][idx]['min_max']['max'] = int(round(shows_0['shows']['items'][idx]['min_max']['max'] - (shows_0['shows']['items'][idx]['min_max']['max']%5), 0))

for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['min_max']['min']<5 and shows_0['shows']['items'][idx]['min_max']['max']<6:
        shows_0['shows']['items'][idx]['min_max']['min'] = 0
        shows_0['shows']['items'][idx]['min_max']['max'] = 5

for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['min_max']['min']<5 and shows_0['shows']['items'][idx]['min_max']['max']>6:
        shows_0['shows']['items'][idx]['min_max']['min'] = 5
        shows_0['shows']['items'][idx]['min_max']['max'] = int(round(shows_0['shows']['items'][idx]['min_max']['max'] + 5-(shows_0['shows']['items'][idx]['min_max']['max']%5), 0))
        
#Create uniform duration spans
for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['min_max']['min'] == 0 and shows_0['shows']['items'][idx]['min_max']['max'] == 5:
        shows_0['shows']['items'][idx]['duration_span'] = 'under 5'
    if 5 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 15 and 5 <= shows_0['shows']['items'][idx]['min_max']['max'] <= 15:
        shows_0['shows']['items'][idx]['duration_span'] = '5 to 15'
    if 5 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 15 and 15 <= shows_0['shows']['items'][idx]['min_max']['max'] <= 30:
        shows_0['shows']['items'][idx]['duration_span'] = '15 to 30'
    if 15 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 30 and 15 <= shows_0['shows']['items'][idx]['min_max']['max'] <= 30:
        shows_0['shows']['items'][idx]['duration_span'] = '15 to 30'
    if 15 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 30 and 30 <= shows_0['shows']['items'][idx]['min_max']['max'] <= 45:
        shows_0['shows']['items'][idx]['duration_span'] = '30 to 45'
    if 30 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 45 and 30 <= shows_0['shows']['items'][idx]['min_max']['max'] <= 45:
        shows_0['shows']['items'][idx]['duration_span'] = '30 to 45'
    if 30 <= shows_0['shows']['items'][idx]['min_max']['min'] <= 45 and 45 <= shows_0['shows']['items'][idx]['min_max']['max']:
        shows_0['shows']['items'][idx]['duration_span'] = 'over 45'
    if 45 <= shows_0['shows']['items'][idx]['min_max']['min']:
        shows_0['shows']['items'][idx]['duration_span'] = 'over 45'

#Check that all every shows are assigned to a span
for idx, show in enumerate(shows_0['shows']['items']):
    try:
        print(Fore.GREEN+ shows_0['shows']['items'][idx]['name'], shows_0['shows']['items'][idx]['duration_span'])
    except KeyError:
        print(Fore.RED + 'span does not exist')
        
##Filter shows by duration
for idx, show in enumerate(shows_0['shows']['items']):
    if shows_0['shows']['items'][idx]['duration_span'] == time_choice:
        print(Fore.CYAN + show['name'], Fore.MAGENTA + show['duration_span'])

############## PARTIE EPISODE ###################################

# Implémentation du mot exact dans la fonction search
query = f'{search_word}' 
test1 = sp.search(q=query, limit=50, type='episode', market='FR')

# Filtrer les épisodes selon la durée
selected_episodes = [episode for episode in test1['episodes']['items'] if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == 'fr']

# Récupérer davantage d'épisodes
offset = 50
while len(selected_episodes) < 3 and offset < test1['episodes']['total']:
    results = sp.search(q=query, limit=50, type='episode', market='FR', offset=offset)
    episodes = results['episodes']['items']
    selected_episodes += [episode for episode in episodes if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == 'fr']
    offset += 50
    
    
# RE RUN ICI  
# Envoi des épisodes sélectionnés à Telegram
if len(selected_episodes) >= 3:
    messagefinal = "Voici une liste de plusieurs podcasts correspondant à votre recherche :\n\n"
    for episode in selected_episodes[:3]:
        messagefinal += f"{episode['name']}\n{episode['external_urls']['spotify']}\n\n" 
elif len(selected_episodes) < 3:
    messagefinal = "Aucune émission ne correspond à votre thème.\nVeuillez entrer un autre thème." #relancer fonction de recherche
send_telegram_message(messagefinal)

    
# Envoi des épisodes sélectionnés à Telegram
if len(selected_episodes) >= 3:
   messagefinal = "Voici une liste de plusieurs podcasts correspondant à votre recherche :\n\n"
   for episode in selected_episodes[:3]:
       messagefinal += f"{episode['name']}\n{episode['external_urls']['spotify']}\n\n" 
send_telegram_message(messagefinal)
