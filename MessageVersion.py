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
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth



# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather
chat_id = "5561504638" #obtenu en allant sur https://api.telegram.org/bot{TOKEN_telegram}/getUpdates

# AUTHENTIFICATION spotipy
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))
     

# fonction pour envoyer un message à Telegram
def send_telegram_message(message): # demander à Jason pour fonction propre
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)

    
# Type d'écoute
send_telegram_message("Que préférez-vous ?\n1. Recevoir une liste de podcasts à écouter en une fois.\n 2. Recevoir une liste de show dont les longueurs des épisodes seront proches de votre temps d'écoute quotidien.")
send_telegram_message("Entrez le numéro correspondant à votre choix : ")

time.sleep(10)

# récupérer la réponse de l'utilisateur
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates") 
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
type_choice = int(text)


# Demande du temps d'écoute souhaité
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
   min_duration = 0
   max_duration = 300000
elif time_choice == 2:
   min_duration = 300000
   max_duration = 900000
elif time_choice == 3:
   min_duration = 900000
   max_duration = 1800000
elif time_choice == 4:
   min_duration = 1800000
   max_duration = 2700000
elif time_choice == 5:
   min_duration = 2700000
   max_duration = 10**1000
   
   
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
    

# Demande de la langue d'écoute
send_telegram_message("Quelle langue souhaitez-vous pour vos podcasts ?\n\nVoici les différents codes : Français=fr, Allemand=de, Anglais=en, Espagnol=es, Italien=it")
send_telegram_message("Entrez le code correspondant à votre choix : ")


time.sleep(15)

# Récupérer la ou les langue(s) entrée(s) sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
language = str(text)


# Demande de mot clé à l'utilisateur
send_telegram_message("Quel type de podcasts souhaitez-vous écouter ?\nEntrez le thème de votre choix : ")
   
time.sleep(15)

# Récupérer le mot exact entré sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
search_word = str(text)
search_word = re.sub(r' ', '', search_word)


############### PARTIE SHOW #####################################


############## PARTIE EPISODE ###################################

if type_choice == 1:
    super_episode = sp.search(q=f'{search_word}', limit=50, type='episode', market='FR') # Implémentation du mot exact dans la fonction search
    selected_episodes = [episode for episode in super_episode['episodes']['items'] if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == f'{language}']
    offset = 50
    while len(selected_episodes) < 4 and offset < super_episode['episodes']['total']:
        results = sp.search(q=f'{search_word}', limit=50, type='episode', market='FR', offset=offset)
        episodes = results['episodes']['items']
        selected_episodes += [episode for episode in episodes if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == f'{language}']
        offset += 50
        messagefinal = "Voici une liste de plusieurs podcasts correspondant à votre recherche :\n\n"
        for episode in selected_episodes[:3]:
            messagefinal += f"{episode['name']}\n{episode['external_urls']['spotify']}\n\n"
            send_telegram_message(messagefinal)

