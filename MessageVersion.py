#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:41:17 2023

@author: lyna
"""

# S'assurer d'avoir fait "%reset" dans la console au début

import spotipy # la librairie pour manipuler l'api spotify
import time
from spotipy.oauth2 import SpotifyClientCredentials
from show_treatment import find_shows
from fonctions import find_episode
from TelegramMessages import send_telegram_message, get_telegram_response


# Demande du chat_id
chat_id = input('Démarrez une conversation avec "userinfobot" sur Telegram.\nEntrez votre ID ici :')

# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather

# AUTHENTIFICATION spotipy
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))
    
# Type d'écoute
send_telegram_message("Que préférez-vous ?\n1. Recevoir une liste de podcasts à écouter en une fois.\n 2. Recevoir une liste de show dont les longueurs des épisodes seront proches de votre temps d'écoute quotidien.", chat_id, TOKEN_telegram)
send_telegram_message("Entrez le numéro correspondant à votre choix : ", chat_id, TOKEN_telegram)

time.sleep(20)

# récupérer la réponse de l'utilisateur
telegram_response = get_telegram_response(TOKEN_telegram)
type_choice = int(telegram_response)

# Demande du temps d'écoute souhaité
send_telegram_message("Quel est le temps d'écoute que vous souhaitez ?\n1. Moins de 5 minutes\n2. De 5 à 15 minutes\n3. De 15 à 30 minutes\n4. De 30 à 45 minutes\n5. Plus de 45 minutes", chat_id, TOKEN_telegram)
send_telegram_message("Entrez le numéro correspondant à votre choix : ", chat_id, TOKEN_telegram)

time.sleep(20)

# récupérer la réponse de l'utilisateur
telegram_response = get_telegram_response(TOKEN_telegram)
time_choice = int(telegram_response)

# Demande de mot clé à l'utilisateur
send_telegram_message("Quel type de podcasts souhaitez-vous écouter ?\nEntrez le thème de votre choix : ", chat_id, TOKEN_telegram)
   
time.sleep(20)

# Récupérer la réponse de l'utilisateur
telegram_response = get_telegram_response(TOKEN_telegram)
search_word = str(telegram_response)

############## PARTIE EPISODE ###################################
if type_choice == 1:
    find_episode(search_word, time_choice)

############### PARTIE SHOW #####################################
if type_choice == 2:
    find_shows(search_word, time_choice, chat_id, TOKEN_telegram)
