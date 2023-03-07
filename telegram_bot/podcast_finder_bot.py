# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:41:16 2023

@author: Jason
"""

import os
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

BOT_TOKEN = '5928162912:AAEujI4qI49nAuyx3n4VIhdQFtPN5jy4JTc'


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Liste de podcasts à écouter en une fois', callback_data='m1')],
                [InlineKeyboardButton('Liste de show dont les épisodes seront proches de votre temps d\'écoute quotidien', callback_data='m2')]]
    return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Moins de 5 minutes', callback_data='1')],
                [InlineKeyboardButton('De 5 à 15 minutes', callback_data='2')],
                [InlineKeyboardButton('De 15 à 30 minutes', callback_data='3')],
                [InlineKeyboardButton('De 30 à 45 minutes', callback_data='4')],
                [InlineKeyboardButton('Plus de 45 minutes', callback_data='5')]]
    return InlineKeyboardMarkup(keyboard)

def third_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Français', callback_data='fr')],
                [InlineKeyboardButton('Anglais', callback_data='en')],
                [InlineKeyboardButton('Espagnol', callback_data='es')],
                [InlineKeyboardButton('Italien', callback_data='it')]
                [InlineKeyboardButton('Allemand', callback_data='de')]]
    return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message():
    return 'Que préférez-vous ?'

def second_menu_message():
    return 'Quel est le temps d\'écoute que vous souhaitez ?'

def third_menu_message():
    return 'Quelle langue souhaitez-vous pour vos podcasts ?'

def fourth_menu_message():
    return 'Quel type de podcasts souhaitez-vous écouter ?\nEntrez le thème de votre choix :'

############################# Handlers #########################################
def start(update, context):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())

def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=second_menu_message(),
                            reply_markup=second_menu_keyboard())

def second_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=third_menu_message(),
                            reply_markup=third_menu_keyboard())

def third_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=fourth_menu_message())

def fourth_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Vous avez choisi le thème : " + query.data)


updater = Updater(BOT_TOKEN, use_context=True)

# Handlers

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern='m2_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(fourth_menu, pattern='m2_3'))

# Start the bot
updater.start_polling()
updater.idle()

