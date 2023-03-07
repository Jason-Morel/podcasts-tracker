#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:58:42 2023

@author: lyna
"""
import requests
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))

TOKEN_telegram = 0
chat_id = 0

def send_telegram_message(message): 
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    


time_choice = 1

def range_for_episode(time):
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

    return min_duration, max_duration

def range_for_show(time):
    if time_choice == 1:
        return 'under 5'
    elif time_choice == 2:
        return '5 to 15'
    elif time_choice == 3:
        return '15 to 30'
    elif time_choice == 4:
        return '30 to 45'
    elif time_choice == 5:
        return 'over 45'
    
    
def find_episode(key, min_d, max_d):    
    global sp
    min_duration = 0
    max_duration = 1
    search_word = 0
    
    super_episode = sp.search(q=f'{search_word}', limit=50, type='episode', market='FR') # Implémentation du mot exact dans la fonction search
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
    send_telegram_message(messagefinal)