from random import randint
import sys
import telebot   
import os   
import io   
import pandas as pd
import requests
import json
import time
import re
from random import *

CHAVE_API_TELEGRAM = "5570452334:AAHmIZApvbKb1wd8hSiOj6BKu6-TNMINd-8"

bot = telebot.TeleBot(CHAVE_API_TELEGRAM)

user = bot.get_me()
updates = bot.get_updates()

def jogo(msg):
    menu  ='|              |    Confessa    |  Não Confessa |'
    menu2 ='|--------------|----------------|---------------|'
    menu3 ='|    Confessa  |     10;10      |      0;30     |'
    menu4 ='| Não Confessa |      0;30      |      5;5      |'
    menu5 ='-------------------------------------------------'
    
    nome =  '                             Bonnie             '
    
    response = nome.center(80, ' ') + '\n'
    response += menu5.center(80, ' ') + '\n'
    response += menu.center(80, ' ') + '\n'
    response += menu2.center(80, ' ') + '\n'
    response += menu3.center(80, ' ') + '\n'
    response += '\t\tCleyde' + menu2.center(40, ' ') + '\n'
    response += menu4.center(80, ' ') + '\n'
    response += menu5.center(80, ' ') + '\n'
    
    Bonnie = int(msg.text)
    Cleyde = randint(1,2)
    
    if Cleyde ==1:
        response += "Cleyde decidiu Confessar.\n"
    elif Cleyde ==2:
        response += "Cleyde decidiu NÃO CONFESSAR.\n"
    
    if Bonnie==1 and Cleyde==1:
        response += 'Ambos os  dissidiram Confessar.\nLogo, ambos vão passar 10 anos de cadeia.\n'
        response += 'Este é o Equilíbrio de Nash deste jogo.'
    
    elif Bonnie==2 and Cleyde==2:
        response += 'Bonnie e Cleyde  dissidiram Não Confessar.\nLogo, ambos vão passar 5 anos de cadeia.\n'
        response += 'Esta jogada seria a melhor para os dois.'
    
    elif Bonnie==2 and Cleyde==1:
        response += 'Bonnie vai para a cadeia durante 30 anos e Cleyde vai sair livre da cadeia\n'
    
    else:
        response += 'Cleyde vai para a cadeia durante 30 anos e Bonnie vai sair livre da cadeia\n'
    
    return response

@bot.message_handler(func=lambda msg: msg.text is not None)
def handle_message(message):
    response = jogo(message)
    bot.reply_to(message, response)

bot.polling()
