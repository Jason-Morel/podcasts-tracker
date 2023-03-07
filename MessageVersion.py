#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:41:17 2023

@author: lyna
"""

# S'assurer d'avoir fait "%reset" dans la console au début

import tkinter as tk
import spotipy # la librairie pour manipuler l'api spotify
from spotipy.oauth2 import SpotifyClientCredentials
from show_treatment import find_shows
from episode_treatment import find_episode

# Demande du chat_id
chat_id = input('\n\n\nDémarrez une conversation avec "userinfobot" sur Telegram.\nEntrez votre ID ici :')

# Infos de mon telegram :
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather

# AUTHENTIFICATION spotipy
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='e48f42372a074a25b7a0d25da48439d6',
                                                                         client_secret='90eb460ff94847998926f6d380532f59'))
    

# Fonction appelée lors de la soumission du formulaire
def submit_form():
    # Récupération des valeurs sélectionnées par l'utilisateur
    type_choice = type_var.get()
    time_choice = time_var.get()
    search_word = search_entry.get()
    
    ############## PARTIE EPISODE ###################################
    if type_choice == 1:
        find_episode(search_word, time_choice, chat_id, TOKEN_telegram)

    ############### PARTIE SHOW #####################################
    if type_choice == 2:
        find_shows(search_word, time_choice, chat_id, TOKEN_telegram)

# Création de la fenêtre et des widgets
root = tk.Tk()
root.title("Choix de podcasts")

type_label = tk.Label(root, text="Que préférez-vous ?").pack(pady=10)
type_var = tk.IntVar()
type1_radio = tk.Radiobutton(root, text="Recevoir une liste de podcasts à écouter en une fois.", variable=type_var, value=1).pack(anchor='w')
type2_radio = tk.Radiobutton(root, text="Recevoir une liste de show dont les longueurs des épisodes seront proches de votre temps d'écoute quotidien.", variable=type_var, value=2).pack(anchor='w')

time_label = tk.Label(root, text="Quel est le temps d'écoute que vous souhaitez ?").pack(pady=10)
time_var = tk.IntVar()
time1_radio = tk.Radiobutton(root, text="Moins de 5 minutes", variable=time_var, value=1).pack(anchor='w')
time2_radio = tk.Radiobutton(root, text="De 5 à 15 minutes", variable=time_var, value=2).pack(anchor='w')
time3_radio = tk.Radiobutton(root, text="De 15 à 30 minutes", variable=time_var, value=3).pack(anchor='w')
time4_radio = tk.Radiobutton(root, text="De 30 à 45 minutes", variable=time_var, value=4).pack(anchor='w')
time5_radio = tk.Radiobutton(root, text="Plus de 45 minutes", variable=time_var, value=5).pack(anchor='w')

search_label = tk.Label(root, text="Quel type de podcasts souhaitez-vous écouter ?").pack(pady=10)
search_entry = tk.Entry(root)
search_entry.pack()

submit_button = tk.Button(root, text="Valider", command=submit_form).pack(pady=10)

root.mainloop()

# Fin de la conversation
print('\nVous pouvez aller sur votre compte Telegram pour découvrir le résultat de votre demande')