from random import randint
from random import choice
import sys
import telebot   
import pandas as pd
import requests
import json
import time
import re
import random

CHAVE_API_TELEGRAM = "5570452334:AAHmIZApvbKb1wd8hSiOj6BKu6-TNMINd-8"

bot = telebot.TeleBot(CHAVE_API_TELEGRAM)

user = bot.get_me()
updates = bot.get_updates()

players = {}
scores = {}
round_number = 0

def welcome_message(message):
    text = "Bem-vindo ao jogo do dilema dos prisioneiros!\n\n" \
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'. Se ambos cooperarem, ambos recebem uma sentença de 1 ano. Se ambos traírem, ambos recebem uma sentença de 2 anos. Se um cooperar e o outro trair, o traidor recebe uma sentença reduzida de 6 meses e o cooperador recebe uma sentença aumentada de 3 anos.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /jogarsozinho. Para jogar contra outros jogadores, digite /jogar."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message(message)

@bot.message_handler(commands=['jogar'])
def jogar_message(message):
    text = "Escolha o tipo de jogo que você deseja jogar:\n\n" \
           "1. Contra a máquina (/jogarsozinho)\n" \
           "2. Contra outros jogadores\n\n" \
           "Digite o número correspondente:"
    bot.send_message(message.chat.id, text)
    
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
        opponent_decision = choice(["cooperar", "trair"])
        players[player_id]["opponent_decision"] = opponent_decision
        bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
    else:
        bot.send_message(player_id, "Você já está jogando contra outro jogador!")

# Lista de jogadores disponíveis
jogadores_disponiveis = []

# Comando /multiplayer
@bot.message_handler(commands=['multiplayer'])
def multiplayer_message(message):
    if len(jogadores_disponiveis) < 2:
        bot.send_message(message.chat.id, "Desculpe, não há jogadores suficientes disponíveis no momento.")
    else:
        # Escolher dois jogadores aleatoriamente
        jogador1, jogador2 = random.sample(jogadores_disponiveis, 2)
        # Remover os jogadores escolhidos da lista de jogadores disponíveis
        jogadores_disponiveis.remove(jogador1)
        jogadores_disponiveis.remove(jogador2)
        # Iniciar o jogo entre os dois jogadores conectados
        jogo(jogador1, jogador2)

# Função para adicionar jogadores à lista de jogadores disponíveis
def adicionar_jogador(jogador):
    jogadores_disponiveis.append(jogador)
    bot.send_message(jogador, "Você foi adicionado à lista de jogadores disponíveis para jogar.")

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
                random_decision = choice(["cooperar", "trair"])
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