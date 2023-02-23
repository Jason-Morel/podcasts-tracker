# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:56:49 2023

@author: Jason
"""

import spotipy # la librairie pour manipuler l'api spotify
import spotipy.util as util
import requests
import re
import pandas as pd

# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather
chat_id = "5561504638" #obtenu en allant sur https://api.telegram.org/bot{TOKEN_telegram}/getUpdates

# AUTHENTIFICATION spotipy
username="31aon4o2j7wikppjnfxfvpvptjtu?si=442993df78a74794"
clientId= "e48f42372a074a25b7a0d25da48439d6"
clientSecret="90eb460ff94847998926f6d380532f59"
 
scope = 'playlist-modify-public'

token = util.prompt_for_user_token(username,scope,client_id=clientId,client_secret=clientSecret,redirect_uri='https://github.com/Jason-Morel/podcasts-tracker')

if token:
     sp = spotipy.Spotify(auth=token)
     sp.trace = False


# fonction pour envoyer un message à Telegram
def send_telegram_message(message): # demander à Jason pour fonction propre
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    

    # Demande du temps d'écoute souhaité
    
# envoyer les messages à Telegram
send_telegram_message("Quel est le temps d'écoute que vous souhaitez ?\n\n1. Moins de 5 minutes\n2. De 5 à 10 minutes\n3. De 10 à 15 minutes\n4. De 15 à 20 minutes\n5. De 20 à 30 minutes\n6. De 30 à 45 minutes\n7. De 45 minutes à 1 heure\n8. Plus d'une heure")

# demander à l'utilisateur de saisir leur choix via Telegram
send_telegram_message("Entrez le numéro correspondant à votre choix : ")

# RE RUN À PARTIR D'ICI

# récupérer la réponse de l'utilisateur
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates") #Demander à Jason pour fonction
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
time_choice = int(text)

# envoyer le temps d'écoute choisi depuis votre bot
send_telegram_message(f"Réponse choisie : {time_choice}")

if time_choice == 1:
   min_duration = 0
   max_duration = 300
elif time_choice == 2:
   min_duration = 300
   max_duration = 600
elif time_choice == 3:
   min_duration = 600
   max_duration = 900
elif time_choice == 4:
   min_duration = 900
   max_duration = 1200
elif time_choice == 5:
   min_duration = 1200
   max_duration = 1800
elif time_choice == 6:
   min_duration = 1800
   max_duration = 2700
elif time_choice == 7:
   min_duration = 2700
   max_duration = 3600
elif time_choice == 8:
   min_duration = 3600
   max_duration = 10**10
   
# Demande de mot clé à l'utilisateur
send_telegram_message("Quel type de podcast souhaitez-vous écouter aujourd'hui ?\nEntrez le thème de votre choix : ")
   
# Récupérer le mot exact entré sur Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
data = response.json()
result = data["result"][-1]
text = result["message"]["text"]
search_word = str(text)
search_word = re.sub(r' ', '', search_word)

# Implémentation du mot exact dans la fonction search
query = f'^{search_word}$' # un peu perplexe
test1 = sp.search(q=query, limit=50, type='show', market='FR')



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

#1-Add a new key (called 'episodes') to the shows_0['shows']['items'][idx] dictionaries. It's a dictionary which contains descriptions of the show's first 50 episodes.
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['episodes'] = sp.show_episodes(show_id=shows_0['shows']['items'][idx]['id'], limit=50, market='FR')

#2-Add a new key (called 'duration_ms') to the shows_0['shows']['items'][idx] dictionaries. It's a list which contains durations (in ms) of the show's first 50 episodes. 
for idx, show in enumerate(shows_0['shows']['items']):
    duration_ms = []
    for i, episode in enumerate(shows_0['shows']['items'][idx]['episodes']['items']):
        duration_ms.append(shows_0['shows']['items'][idx]['episodes']['items'][i]['duration_ms'])
        shows_0['shows']['items'][idx]['durations_ms'] = duration_ms
    
#3-Find min and max values of the duration_ms list
#3.1-Convert lists into Pandas DataFrames
for idx, show in enumerate(shows_0['shows']['items']):
    shows_0['shows']['items'][idx]['durations_ms'] = pd.DataFrame({'duration_ms':shows_0['shows']['items'][idx]['durations_ms']})
#Add a new key (called 'min_max') to the shows_0['shows']['items'][idx] dictionaries. It's a dictionary which contains the min (10th percentile) and max (90th percentile) of the show's first 50 episodes. 
for idx, show in enumerate(shows_0['shows']['items']):
    durations_ms = shows_0['shows']['items'][idx]['durations_ms']
    shows_0['shows']['items'][idx]['min_max'] = {'min':round(int(durations_ms.quantile(q=0.1))/60000,2), 'max':round(int(durations_ms.quantile(q=0.9))/60000,2)} #min and max are converted to minutes

#To have an idea of the intervals we can expect with this method:
for idx, show in enumerate(shows_0['shows']['items']):
    print(shows_0['shows']['items'][idx]['min_max'])