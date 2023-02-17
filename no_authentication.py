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

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

#Try to find 10 shows related to economy in French market
shows = sp.search(q='économie', limit=10, type='show', market='FR')
