#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:48:54 2023

@author: lyna
"""
import os
import spotipy
import spotipy.util as util
import sys

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
    
    

# PREMIER TEST
# code très redondant mais ce n'est qu'un premier jet

    # Demande du temps d'écoute souhaité
    print("Quel est le temps d'écoute que vous souhaitez ?")
    print("1. Moins de 5 minutes")
    print("2. De 5 à 10 minutes")
    print("3. De 10 à 15 minutes")
    print("4. De 15 à 20 minutes")
    print("5. De 20 à 30 minutes")
    print("6. De 30 à 45 minutes")
    print("7. De 45 minutes à 1 heure")
    print("8. Plus d'une heure")

    time_choice = int(input("Entrez le numéro correspondant à votre choix : "))

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

    # Demande de la catégorie souhaitée
    results = sp.categories(limit=100)
    categories = results['categories']['items']
    # ici la variable "results" est la réponse renvoyée par l'API Spotify quand on fait une demande pour récupérer les catégories.
    # Le dictionnaire "results" contient pleins d'infos et nous on garde la clé "categories" et la sous-clé "items".
    # Le code stocke la liste des catégories dans la variable "categories".

    print("Quelle catégorie de podcast préférez-vous ?")
    for i, category in enumerate(categories): #fonction "enumerate" : renvoie à chaque tour un compteur et un élément de la liste
        print(f"{i + 1}. {category['name']}")
    #affiche à chaque tour l'index de la catégorie + son nom, qui est accessible via la clé "name" du dictionnaire "category". 

    category_index = int(input("Entrez le numéro correspondant à votre choix : "))

# problème : cela propose les catégories de musiques mais pas de podcast