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
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu. Para jogar contra outros jogadores, digite /multiplayer."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message(message)

@bot.message_handler(commands=['cpu'])
def jogar_so_mensagem(message):
    player_id = message.from_user.id

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
        scores[player_id] = 0
        bot.send_message(player_id, "Digite 'cooperar' ou 'trair' para jogar contra a CPU!")
    else:
        bot.send_message(player_id, "Você já está jogando contra a CPU, digite 'cooperar' ou 'trair' para continuar o jogo!")

    @bot.message_handler(func=lambda message: True)
    def process_decision(message):
        decision = message.text.lower().strip()
        if decision == "cooperar" or decision == "trair":
            player_id = message.from_user.id
            players[player_id]["decision"] = decision
            opponent_decision = choice(["cooperar", "trair"])
            players[player_id]["opponent_decision"] = opponent_decision
            if decision == "cooperar" and opponent_decision == "cooperar":
                scores[player_id] += 3
                bot.send_message(player_id, "Você escolheu cooperar e o seu oponente também. Ambos ganharam 3 pontos!")
            elif decision == "cooperar" and opponent_decision == "trair":
                scores[player_id] -= 1
                bot.send_message(player_id, "Você escolheu cooperar e o seu oponente traiu. Você perdeu 1 ponto!")
            elif decision == "trair" and opponent_decision == "cooperar":
                scores[player_id] += 5
                bot.send_message(player_id, "Você escolheu trair e o seu oponente cooperou. Você ganhou 5 pontos!")
            else:
                scores[player_id] -= 2
                bot.send_message(player_id, "Você escolheu trair e o seu oponente também. Ambos perderam 2 pontos!")
            bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}. Sua pontuação atual é {scores[player_id]}.")
            bot.send_message(player_id, "Digite 'cooperar' ou 'trair' para jogar novamente!")
        else:
            bot.send_message(player_id, "Opção inválida, digite 'cooperar' ou 'trair' para jogar contra a CPU!")

def fim_de_jogo(player_id, opponent_id):
    global players, scores, round_number
    round_number = 0
    player_score = scores[player_id]
    opponent_score = scores[opponent_id]
    player_name = players[player_id]["name"]
    opponent_name = players[opponent_id]["name"]
    text = f"Fim de jogo!\n\n{player_name}: {player_score} pontos\n{opponent_name}: {opponent_score} pontos\n\n"
    if player_score > opponent_score:
        text += f"{player_name} é o vencedor!"
    elif opponent_score > player_score:
        text += f"{opponent_name} é o vencedor!"
    else:
        text += "O jogo terminou em empate!"
    bot.send_message(player_id, text)
    bot.send_message(opponent_id, text)
    players.pop(player_id)
    players.pop(opponent_id)
    scores.pop(player_id)
    scores.pop(opponent_id)

def iniciar_jogo(player_id, opponent_id, decision):
    global round_number
    
    opponent_decision = players[opponent_id]["decision"]
    
    # Verificar as decisões de ambos os jogadores
    if decision == "cooperar" and opponent_decision == "cooperar":
        players[player_id]["sentenca"] = 1
        players[opponent_id]["sentenca"] = 1
        scores[player_id] += 1
        scores[opponent_id] += 1
    elif decision == "cooperar" and opponent_decision == "trair":
        players[player_id]["sentenca"] = 3
        players[opponent_id]["sentenca"] = 0.5
        scores[player_id] -= 2
        scores[opponent_id] += 2
    elif decision == "trair" and opponent_decision == "cooperar":
        players[player_id]["sentenca"] = 0.5
        players[opponent_id]["sentenca"] = 3
        scores[player_id] += 2
        scores[opponent_id] -= 2
    elif decision == "trair" and opponent_decision == "trair":
        players[player_id]["sentenca"] = 2
        players[opponent_id]["sentenca"] = 2
        scores[player_id] -= 1
        scores[opponent_id] -= 1
    
    # Incrementar o número de rodadas
    round_number += 1
    
    # Enviar mensagens aos jogadores com os resultados da rodada
    bot.send_message(player_id, f"Na rodada {round_number}:\n\n"
                                f"Você jogou: {decision}\n"
                                f"O seu oponente jogou: {opponent_decision}\n"
                                f"Você recebeu uma sentença de {players[player_id]['sentenca']} anos\n"
                                f"Placar atual: {scores[player_id]} x {scores[opponent_id]}")
    bot.send_message(opponent_id, f"Na rodada {round_number}:\n\n"
                                   f"Você jogou: {opponent_decision}\n"
                                   f"O seu oponente jogou: {decision}\n"
                                   f"Você recebeu uma sentença de {players[opponent_id]['sentenca']} anos\n"
                                   f"Placar atual: {scores[opponent_id]} x {scores[player_id]}")
    
    # Limpar as decisões dos jogadores
    players[player_id]["decision"] = None
    players[opponent_id]["decision"] = None
    
    # Verificar se o jogo acabou
    if round_number >= 5:
        fim_de_jogo(player_id, opponent_id)

# Lista de jogadores disponíveis
jogadores_disponiveis = []

# Comando /multiplayer
@bot.message_handler(commands=['multiplayer'])
def multiplayer_message(message):
    if len(jogadores_disponiveis) < 2:
        bot.send_message(message.chat.id, "Desculpe, não há jogadores suficientes disponíveis no momento.")
    else:
        # Escolher dois jogadores aleatoriamente
        jogador1, jogador2 = random.sample(jogadores_disponiveis, k=2)
        players[jogador1]["opponent_id"] = jogador2
        players[jogador2]["opponent_id"] = jogador1

        bot.send_message(jogador1, "Você está jogando contra " + players[jogador2]["name"])
       
    # Encerrar o jogo e enviar a pontuação final
    bot.send_message(jogador1, "O jogo acabou!")
    bot.send_message(jogador1, f"Sua pontuação final é: {scores[jogador1]}")
    bot.send_message(jogador2, "O jogo acabou!")
    bot.send_message(jogador2, f"Sua pontuação final é: {scores[jogador2]}")
    
    # Remover jogadores e pontuações
    del players[jogador1]
    del players[jogador2]
    del scores[jogador1]
    del scores[jogador2]
    
    # Remover jogadores disponíveis
    if jogador1 in jogadores_disponiveis:
        jogadores_disponiveis.remove(jogador1)
    if jogador2 in jogadores_disponiveis:
        jogadores_disponiveis.remove(jogador2)

@bot.message_handler(commands=['pontuacao'])
def pontuacao_message(message):
    text = "Pontuações:\n\n"
    for player_id, score in scores.items():
        player_name = players[player_id]["name"]
        text += f"{player_name}: {score}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def jogo_message(message):
    player_id = message.from_user.id

    # Verificar se o jogador já está jogando contra outro jogador
    if player_id in players:
        bot.send_message(player_id, "Você já está jogando contra outro jogador!")
        return

    # Verificar se o jogador já escolheu uma opção
    decision = message.text.lower().strip()
    if decision not in ["cooperar", "trair"]:
        bot.send_message(player_id, "Escolha inválida. Digite 'cooperar' ou 'trair'.")
        return
    
    # Adicionar jogador à lista de jogadores disponíveis
    if player_id not in jogadores_disponiveis:
        jogadores_disponiveis.append(player_id)
        bot.send_message(player_id, "Aguardando por outro jogador...")
        return
    
    # Escolher oponente aleatório
    opponent_id = random.choice([pid for pid in jogadores_disponiveis if pid != player_id])
    
    # Iniciar o jogo entre o jogador e o oponente
    iniciar_jogo(player_id, opponent_id, decision)
    
if __name__ == "__main__":
    bot.polling()
