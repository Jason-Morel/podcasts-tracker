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

#We need to figure out how to convert a user input into a regular expression.

#Find shows related to economy in French market
shows_0 = sp.search(q='économie', limit=50, type='show', market='FR')
for idx, show in enumerate(shows_0['shows']['items']):
    print(show['publisher'], ':', show['name'], show['languages'], show['id'])

#Find the next 50 shows related to economy in French market (if none of the first 50 episodes matches the expected duration)
shows_50 = sp.search(q='économie', limit=50, offset=50, type='show', market='FR')
for idx, show in enumerate(shows_50['shows']['items']):
    print(show['publisher'], ':', show['name'], show['languages'], show['id'])
#TO DO: add the results on top of the first dictionary instead of creating a new variable


##Look at the distribution of the variable duration_ms for the set of episodes

#1-Add a new key (called 'episodes') to the shows_0['shows']['items'][idx] dictionaries. It contains descriptions of the show's first 50 episodes.
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['episodes'] = sp.show_episodes(show_id=shows_0['shows']['items'][idx]['id'], limit=50, market='FR')

#2-Add a new key (called 'duration_ms') to the shows_0['shows']['items'][idx] dictionaries. It contains durations (in ms) of the show's first 50 episodes. 
for idx, show in enumerate(shows_0['shows']['items']):
    duration_ms = []
    for i, episode in enumerate(shows_0['shows']['items'][idx]['episodes']['items']):
        duration_ms.append(shows_0['shows']['items'][idx]['episodes']['items'][i]['duration_ms'])
        shows_0['shows']['items'][idx]['durations_ms'] = duration_ms
    
#3-Find min and max values of the duration_ms list


    




#Because people usually commute twice a day (home -> office AND office -> home): we could return episodes matching the duration selected by user AND episodes which are twice as long.
#It would allow the user to listen half of the episode in the morning and the other half in the evening.

#How can we approximate episodes duration if API limits the results to 50?
#We could look at the distribution of episodes duration for a specific show.
#Then we would recommend shows to user (instead of episodes).
#It means our tool would not need to be used everyday. Instead, user could use our tool when they feel like discovering new shows which match a specific topic.