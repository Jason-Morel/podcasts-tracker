# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:45:28 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import categories

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id="e48f42372a074a25b7a0d25da48439d6", client_secret="90eb460ff94847998926f6d380532f59")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Identifier les différentes catégories de podcasts
categories = categories(country = "FR", locale = "FR")
