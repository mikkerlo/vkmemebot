import logging
import sys
import time

import telebot
from telebot import types

API_TOKEN = '737388157:AAHEC8sdGNFrk0rloaSTxfUlUvcGedqHWy8'

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)




def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
