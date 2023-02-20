# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:45:28 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Authentication - without user
##We need to figure out how to secure the authentication! (keep id and secret in a different file and add a .gitignore)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e48f42372a074a25b7a0d25da48439d6",
                                                           client_secret="90eb460ff94847998926f6d380532f59"))

#Example - how to use search function
results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

#Find 10 shows related to economy in French market
shows = sp.search(q='économie', limit=10, type='show', market='FR')
for idx, show in enumerate(shows['shows']['items']):
    print(show['publisher'], ':', show['name'])
    
#Find 10 shows related to history in French market
shows_history = sp.search(q='histoire', limit=10, type='show', market='FR')
for idx, show in enumerate(shows_history['shows']['items']):
    print(show['publisher'], ':', show['name'], show['id'])

#Find 10 episodes related to art in French market
shows_art = sp.search(q='art', limit=10, type='episode', market='FR')
for idx, episode in enumerate(shows_art['episodes']['items']):
    print(episode['name'], episode['id'])
    
#Find a show using it's ID
shows_id = sp.show(show_id='2ZFDmgDS2Z6xccP51s1zFQ', market='FR')

#Find episodes using show ID
episode = sp.show_episodes(show_id='2ZFDmgDS2Z6xccP51s1zFQ', limit=50, market='FR')

#Because people usually commute twice a day (home -> office AND office -> home): we could return episodes matching the duration selected by user AND episodes which are twice as long.
#It would allow the user to listen half of the episode in the morning and the other half in the evening.

#How can we approximate episodes duration if API limits the results to 50?
#We could look at the distribution of episodes duration for a specific show.
#Then we would recommend shows to user (instead of episodes).
#It means our tool would not need to be used everyday. Instead, user could use our tool when they feel like discovering new shows which match a specific topic.