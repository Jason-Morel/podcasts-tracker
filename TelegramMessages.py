#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:35:36 2023

@author: lyna
"""

import requests


# info sur telegram
TOKEN_telegram = "6179108053:AAFXqqyrlrLvN_tlSARu2_l3TLXkA_EjXTc" # obtenu en créant notre bot avec le telegram BotFather
#input arbitraire
chat_id = 0

# fonction pour envoyer des messages sur Telegram à un ID donné
def send_telegram_message(message, chat_id, TOKEN_telegram): 
    url = f"https://api.telegram.org/bot{TOKEN_telegram}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    
    return response

# fonction pour récupérer les messages envoyés par l'utilisateur sur Telegram
def get_telegram_response(TOKEN_telegram):
    response = requests.get(f"https://api.telegram.org/bot{TOKEN_telegram}/getUpdates")
    data = response.json()
    result = data["result"][-1]
    text = result["message"]["text"]
    
    return text