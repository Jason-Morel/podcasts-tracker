# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:45:28 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Authentication - without user
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e48f42372a074a25b7a0d25da48439d6",
                                                           client_secret="90eb460ff94847998926f6d380532f59"))

#Example - how to use search function
results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

#Try to find 10 shows related to economy in French market
shows = sp.search(q='économie', limit=10, type='show', market='FR')
for idx, show in enumerate(shows['shows']['items']):
    print(show['publisher'], ':', show['name'])
    
#Try to find 10 shows related to history in French market
shows_history = sp.search(q='histoire', limit=10, type='show', market='FR')
for idx, show in enumerate(shows_history['shows']['items']):
    print(show['publisher'], ':', show['name'], show['id'])

#Try to find 10 episodes related to art in French market
shows_art = sp.search(q='art', limit=10, type='episode', market='FR')
for idx, episode in enumerate(shows_art['episodes']['items']):
    print(episode['name'], episode['id'])