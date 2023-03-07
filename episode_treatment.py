#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:58:42 2023

@author: lyna
"""
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
from TelegramMessages import send_telegram_message

# Authentification spotify
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))
# info sur telegram
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather
#input arbitraire
chat_id = 0

# Défini la durée minimale demandée par l'utilisateur
def min_for_episode(time_choice):
    if time_choice == 1:
        min_duration = 0
    elif time_choice == 2:
        min_duration = 300000
    elif time_choice == 3:
        min_duration = 900000
    elif time_choice == 4:
        min_duration = 1800000
    elif time_choice == 5:
        min_duration = 2700000

    return min_duration

# Défini la durée maximale demandée par l'utilisateur
def max_for_episode(time_choice):
    if time_choice == 1:
        max_duration = 300000
    elif time_choice == 2:
        max_duration = 900000
    elif time_choice == 3:
        max_duration = 1800000
    elif time_choice == 4:
        max_duration = 2700000
    elif time_choice == 5:
        max_duration = 10**1000
        
    return max_duration
    

# trouve une liste d'épisodes selon le thème inscrit, dont la durée est comprise entre la durée minimale et la durée maximale et en français 
# envoie les noms et liens des épisodes à l'utilisateur sur Telegram
   
def find_episode(search_word, time_choice):    
    min_duration = min_for_episode(time_choice)
    max_duration = max_for_episode(time_choice)

    super_episode = sp.search(q=search_word, limit=50, type='episode', market='FR') # Implémentation du mot dans la fonction search
    selected_episodes = [episode for episode in super_episode['episodes']['items'] if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == 'fr']
    offset = 50
    while len(selected_episodes) < 4 and offset < super_episode['episodes']['total']:
        results = sp.search(q=f'{search_word}', limit=50, type='episode', market='FR', offset=offset)
        episodes = results['episodes']['items']
        selected_episodes += [episode for episode in episodes if min_duration <= episode['duration_ms'] <= max_duration and episode['language'] == 'fr']
        offset += 50
    
    messagefinal = "Voici une liste de plusieurs podcasts correspondant à votre recherche :\n\n"
    for episode in selected_episodes[:3]:
        messagefinal += f"{episode['name']}\n{episode['external_urls']['spotify']}\n\n"
    send_telegram_message(messagefinal, chat_id, TOKEN_telegram)
    
    return messagefinal
