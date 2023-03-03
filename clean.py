# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 19:19:28 2023

@author: Jason
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
import os

from no_authentication import get_shows
from no_authentication import authenticate

#Authentication - without user
sp = authenticate()

#Inputs
input_language = 'fr'
input_key_words = 'donut'
input_duration =  '5 to 15'

#Find shows related to input_key_words in input_language market
shows = get_shows(key_words=input_key_words, language=input_language)