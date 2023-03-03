# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:11:02 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
from colorama import Fore, Back, Style

#Authentication - without user
##We need to figure out how to secure the authentication! (keep id and secret in a different file and add a .gitignore)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e48f42372a074a25b7a0d25da48439d6",
                                                           client_secret="90eb460ff94847998926f6d380532f59"))


#Find shows related to economy in French market
shows_0 = sp.search(q='donut', limit=50, type='show', market='FR')
for idx, show in enumerate(shows_0['shows']['items']):
    print(show['languages'])


##Remove shows which are not french
languages = 'fr'
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['languages'] = str(shows_0['shows']['items'][idx]['languages']).lower()
    if re.search(languages, shows_0['shows']['items'][idx]['languages']) == None:
        print(shows_0['shows']['items'][idx]['languages'])
        del shows_0['shows']['items'][idx]
        
#Why aren't all the shows deleted??