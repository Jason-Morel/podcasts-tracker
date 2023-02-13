#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:48:54 2023

@author: lyna
"""

import os
import spotipy
import spotipy.util as util

# AUTHENTIFICATION 

os.environ["SPOTIPY_CLIENT_ID"] = "e48f42372a074a25b7a0d25da48439d6" # ID DE NOTRE SPOTIFY DEVELOPPER
os.environ["SPOTIPY_CLIENT_SECRET"] = "90eb460ff94847998926f6d380532f59" # SECRET DU SPOTIDU DEVELOPPER

username = "31aon4o2j7wikppjnfxfvpvptjtu?si=a9a987029b674187" # USERNAME DANS LE LIEN DE NOTRE COMPTE SPOTIFY
scope = "user-library-read"
redirect_uri = "https://github.com/LaDjazzz/podcasts-tracker" # URI BASIQUE POUR REDIRIGER L'EXÉCUTION
token = util.prompt_for_user_token(username, scope, redirect_uri=redirect_uri)

os.environ["SPOTIPY_REDIRECT_URI"] = "https://github.com/LaDjazzz/podcasts-tracker"
token = util.prompt_for_user_token(username, scope)

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token) # PAS FORCÉMENT COMPRIS LE CODE MAIS C'ÉTAIT DANS LE TUTO
    results = sp.current_playback()
    print(results)
else:
    print("Can't get token for", username)
    
    
    
# EXEMPLE DU SITE SPOTIPY
    
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()


