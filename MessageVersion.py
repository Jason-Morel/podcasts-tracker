#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:41:17 2023

@author: lyna
"""

# S'assurer d'avoir fait "%reset" dans la console au début

import spotipy # la librairie pour manipuler l'api spotify
from spotipy.oauth2 import SpotifyClientCredentials
from show_treatment import find_shows
from episode_treatment import find_episode

# Demande du chat_id
chat_id = input('\n\n\nDémarrez une conversation avec "userinfobot" sur Telegram.\nEntrez votre ID ici :')

# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather

# AUTHENTIFICATION spotipy
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))
    
# Type d'écoute
print("\n\n\nQue préférez-vous ?\n1. Recevoir une liste de podcasts à écouter en une fois.\n2. Recevoir une liste de show dont les longueurs des épisodes seront proches de votre temps d'écoute quotidien.")
type_choice = int(input("\nEntrez le numéro correspondant à votre choix : "))


# Demande du temps d'écoute souhaité
print("\n\n\nQuel est le temps d'écoute que vous souhaitez ?\n1. Moins de 5 minutes\n2. De 5 à 15 minutes\n3. De 15 à 30 minutes\n4. De 30 à 45 minutes\n5. Plus de 45 minutes")
time_choice = int(input("\nEntrez le numéro correspondant à votre choix : "))

# Demande de mot clé à l'utilisateur
search_word = input("\n\n\nQuel type de podcasts souhaitez-vous écouter ?\nEntrez le thème de votre choix : ")

############## PARTIE EPISODE ###################################
if type_choice == 1:
    find_episode(search_word, time_choice, chat_id, TOKEN_telegram)

############### PARTIE SHOW #####################################
if type_choice == 2:
    find_shows(search_word, time_choice, chat_id, TOKEN_telegram)

# Fin de la conversation
print('\nVous pouvez aller sur votre compte Telegram pour découvrir le résultat de votre demande')