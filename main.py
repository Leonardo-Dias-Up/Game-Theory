from random import randint
import sys
import telebot   
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

players = {}
scores = {}
round_number = 0

def jogo(update):
    message = update.message
    player_id = message.from_user.id
    text = message.text.lower()

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None}
        scores[player_id] = 0
        if len(players) == 1:
            opponent_id = player_id
        else:
            return "Você está inscrito no jogo do dilema dos prisioneiros! Aguarde seu oponente."
    else:
        if len(players) == 1:
            opponent_id = player_id
        else:
            opponent_id = [p for p in players if p != player_id][0]
        players[player_id]["opponent_id"] = opponent_id
        players[opponent_id]["opponent_id"] = player_id
        response = f"Você está jogando contra {players[opponent_id]['name']}!"
        bot.send_message(opponent_id, f"{players[player_id]['name']} entrou no jogo do dilema dos prisioneiros! É sua vez de escolher 'cooperar' ou 'trair'.")
        return response
    
@bot.message_handler(commands=['jogarsozinho'])
def jogar_so_mensagem(message):
    player_id = message.from_user.id

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
        scores[player_id] = 0
        bot.send_message(player_id, "Você está jogando contra si mesmo!")
        opponent_decision = random.choice(["cooperar", "trair"])
        players[player_id]["opponent_decision"] = opponent_decision
        bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
    else:
        bot.send_message(player_id, "Você já está jogando contra outro jogador!")


def handle_message(message):
    global round_number
    response = ""
    message_text = message.text.lower()
    player_id = message.from_user.id

    if player_id not in players:
        response = "Você ainda não está inscrito no jogo. Digite /start para entrar no jogo."
    elif players[player_id]["decision"] is None:
        if message_text not in ["cooperar", "trair"]:
            response = "Digite 'cooperar' ou 'trair' para jogar."
        else:
            players[player_id]["decision"] = message_text
            response = "Aguardando decisão do seu oponente..."
            opponent_id = players[player_id]["opponent_id"]
            if opponent_id == player_id:
                random_decision = random.choice(["cooperar", "trair"])
                players[opponent_id]["decision"] = random_decision
                response += f"Você jogou contra si mesmo e escolheu {message_text}. O resultado é: "
            elif players[opponent_id]["decision"] is not None:
                round_number += 1
                p1_decision = players[player_id]["decision"]
                p2_decision = players[opponent_id]["decision"]
                if p1_decision == "cooperar" and p2_decision == "cooperar":
                    scores[player_id] += 1
                    scores[opponent_id] += 1
                    response = "Ambos cooperaram e receberam uma sentença de 1 ano."
                elif p1_decision == "cooperar" and p2_decision == "trair":
                    scores[player_id] -= 1
                    scores[opponent_id] += 3
                    response = f"{players[player_id]['name']} cooperou e {players[opponent_id]['name']} traiu. {players[player_id]['name']} recebeu uma sentença de 3 anos e {players[opponent_id]['name']} recebeu uma sentença reduzida de 6 meses."
                elif p1_decision == "trair" and p2_decision == "cooperar":
                    scores[player_id] += 3
                    scores[opponent_id] -= 1
                    response = f"{players[player_id]['name']} traiu e {players[opponent_id]['name']} cooperou. {players[player_id]['name']} recebeu uma sentença reduzida de 6 meses e {players[opponent_id]['name']} recebeu uma sentença de 3 anos."
                elif p1_decision == "trair" and p2_decision == "trair":
                    scores[player_id] -= 2
                    scores[opponent_id] -= 2
                    response = "Ambos traíram e receberam uma sentença de 2 anos."

                players[player_id]["decision"] = None
                players[opponent_id]["decision"] = None

                if round_number == 5:
                    winner_id = max(scores, key=scores.get)
                    response += f"\n\nJogo finalizado! {players[winner_id]['name']} venceu com {scores[winner_id]} pontos.\n\nDigite /start para jogar novamente."
                    players.clear()
                    scores.clear()
                    round_number = 0

            if opponent_id != player_id:
                bot.send_message(opponent_id, f"Sua vez de escolher 'cooperar' ou 'trair'.")
            bot.reply_to(message, response)

if __name__ == '__main__':
    bot.polling()