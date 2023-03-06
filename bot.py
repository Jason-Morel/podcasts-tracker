# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:17:44 2023

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



############################### Bot ############################################
def start(update, context):
  update.message.reply_text(languages_menu_message(),
                            reply_markup=languages_menu_keyboard())

def languages_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=languages_menu_message(),
                        reply_markup=languages_menu_keyboard())
  
#Insert a function to ask keywords input

def durations_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=durations_menu_message(),
                        reply_markup=durations_menu_keyboard())

def types_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=types_menu_message(),
                        reply_markup=types_menu_keyboard())



############################ Keyboards #########################################
def languages_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Français', callback_data='m1')],
              [InlineKeyboardButton('Anglais', callback_data='m1')],
              [InlineKeyboardButton('Allemand', callback_data='m1')]
              [InlineKeyboardButton('Italien', callback_data='m1')]
              [InlineKeyboardButton('Espagnol', callback_data='m1')]]
  return InlineKeyboardMarkup(keyboard)

def durations_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Moins de 5 minutes', callback_data='m2')],
              [InlineKeyboardButton('De 5 à 15 minutes', callback_data='m2')],
              [InlineKeyboardButton('De 15 à 30 minutes', callback_data='m2')],
              [InlineKeyboardButton('De 30 à 45 minutes', callback_data='m2')],
              [InlineKeyboardButton('Plus de 45 minutes', callback_data='m2')]]
  return InlineKeyboardMarkup(keyboard)

def types_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Episodes', callback_data='m2_1')],
              [InlineKeyboardButton('Shows', callback_data='m2_2')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def languages_menu_message():
  return 'Choisir une langue'

def durations_menu_message():
  return 'Choisir un intervalle de temps'

def types_menu_message():
  return 'Vous recherchez...'

############################# Handlers #########################################
updater = Updater('5928162912:AAEujI4qI49nAuyx3n4VIhdQFtPN5jy4JTc', use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(languages_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(durations_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(types_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))

updater.start_polling()
