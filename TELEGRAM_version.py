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
send_telegram_message("Quel est le temps d'écoute que vous souhaitez ?\n\n1. Moins de 10 minutes\n2. De 10 à 20 minutes\n3. De 20 à 30 minutes\n4. De 30 à 40 minutes\n5. De 40 à 50 minutes\n6. De 50 minutes à 1 heure\n7. Plus d'une heure")

# demander à l'utilisateur de saisir leur choix via Telegram
send_telegram_message("Entrez le numéro correspondant à votre choix : ")

# RE RUN À PARTIR D'ICI

# récupérer la réponse de l'utilisateur
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates") 
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
time_choice = int(text)

# envoyer le temps d'écoute choisi depuis votre bot
send_telegram_message(f"Réponse choisie : {time_choice}")

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
   
# Demande de mot clé à l'utilisateur
send_telegram_message("Quel type de podcast souhaitez-vous écouter aujourd'hui ?\nEntrez le thème de votre choix : ")
   
# Récupérer le mot exact entré sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
search_word = str(text)
search_word = re.sub(r' ', '', search_word)

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


# Automatiser entièrement le bot telegram 
# Changer la langue en fonction de la préférence de l'utilisateur si besoin