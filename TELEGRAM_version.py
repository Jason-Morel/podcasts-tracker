#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:59:41 2023

@author: lyna
"""

import spotipy    # la librairie pour manipuler l'api spotify
import spotipy.util as util
import requests

# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" #obtenu en créant notre bot avec le compte telegram BotFather
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
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    

    # Demande du temps d'écoute souhaité
    
# envoyer les messages à Telegram
message = "Quel est le temps d'écoute que vous souhaitez ?\n\n1. Moins de 5 minutes\n2. De 5 à 10 minutes\n3. De 10 à 15 minutes\n4. De 15 à 20 minutes\n5. De 20 à 30 minutes\n6. De 30 à 45 minutes\n7. De 45 minutes à 1 heure\n8. Plus d'une heure"
send_telegram_message(message)

# demander à l'utilisateur de saisir leur choix via Telegram
send_telegram_message("Entrez le numéro correspondant à votre choix : ")

# RE RUN À PARTIR D'ICI

# récupérer la réponse de l'utilisateur
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
time_choice = int(text)

# envoyer le temps d'écoute choisi à votre bot
message = f"Réponse choisie : {time_choice}"
url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
requests.get(url)


if time_choice == 1:
   min_duration = 0
   max_duration = 300
elif time_choice == 2:
   min_duration = 300
   max_duration = 600
elif time_choice == 3:
   min_duration = 600
   max_duration = 900
elif time_choice == 4:
   min_duration = 900
   max_duration = 1200
elif time_choice == 5:
   min_duration = 1200
   max_duration = 1800
elif time_choice == 6:
   min_duration = 1800
   max_duration = 2700
elif time_choice == 7:
   min_duration = 2700
   max_duration = 3600
elif time_choice == 8:
   min_duration = 3600
   max_duration = 10**10