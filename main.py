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
jogadores_disponiveis = {}

# DESENVOLVEDORES DO BOT
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message, "Desenvolvedores: Leonardo Dias e Djalma. 2023")
    
# BOAS VINDAS
def welcome_message(message):
    text = "Bem-vindo ao jogo do dilema dos prisioneiros!\n\n" \
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu. Para jogar contra outros jogadores, digite /multiplayer."
    bot.send_message(message.chat.id, text)

# INICIO JOGO
@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message(message)

# JOGANDO CONTRA A CPU
@bot.message_handler(commands=['cpu'])
def jogar_so_mensagem(message):
    player_id = message.from_user.id

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
        scores[player_id] = 0
        bot.send_message(player_id, "Digite 'cooperar' ou 'trair' para fazer sua escolha.")
    else:
        bot.send_message(player_id, "Você já está jogando contra si mesmo!")

# DILEMA DOS PRISIONEIROS
@bot.message_handler(func=lambda message: True)
def jogar_contra_cpu(message):
    player_id = message.chat.id

    # Verifica se há jogadores disponíveis
    if len(jogadores_disponiveis) < 2:
        bot.send_message(player_id, "Não há jogadores disponíveis no momento. Tente novamente mais tarde.")
        return

    # Adicionar jogador à lista de jogadores disponíveis
    for player_id in jogadores_disponiveis.keys():
     if not jogadores_disponiveis[player_id]['jogando']:
          jogadores_disponiveis.append(player_id)
          bot.send_message(player_id, "Aguardando por outro jogador...")
          return
    
    # Escolher oponente aleatório
    if jogadores_disponiveis:
          opponent_id = random.choice([pid for pid in jogadores_disponiveis if pid != player_id])
    else:
          bot.send_message(message.chat.id, "Não há jogadores disponíveis no momento.")
    
    # Iniciar o jogo entre o jogador e o oponente
    iniciar_jogo(player_id, opponent_id, player_decision)
    
    # Jogando o oponente
    if player_id in players:
        opponent_id = players[player_id]["opponent_id"]
        if message.text.lower() in ["cooperar", "trair"]:
            players[player_id]["decision"] = message.text.lower()

            if players[opponent_id]["decision"] is not None:
                player_decision = players[player_id]["decision"]
                opponent_decision = choice(["cooperar", "trair"])
                players[player_id]["opponent_decision"] = opponent_decision
                bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")

                if player_decision == "cooperar" and opponent_decision == "cooperar":
                    scores[player_id] += 2
                    bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam 2 pontos!")
                elif player_decision == "cooperar" and opponent_decision == "trair":
                    scores[player_id] -= 1
                    bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu 1 ponto!")
                elif player_decision == "trair" and opponent_decision == "cooperar":
                    scores[player_id] += 3
                    bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou 3 pontos!")
                else:
                    bot.send_message(player_id, "Você e seu oponente traíram. Ninguém ganhou pontos.")

                #bot.send_message(player_id, f"Sua escolha: {player_decision}")
                #bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                bot.send_message(player_id, "Obrigado por jogar o Dilema do Prisioneiro, \
                                  digite /cpu para jogar contra o computador, \
                                 /multiplayer para jogar contra uma pessoa ou digite qualquer outra coisa para sair.")
                players.pop(player_id)
                
# ENCERRANDO O JOGO
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

# INICINANDO O JOGO MULTIPLAYER
def iniciar_jogo(player_id, opponent_id, player_decision):
    global round_number
    
    opponent_decision = players[opponent_id]["decision"]
    
    # Verificar as decisões de ambos os jogadores
    if player_decision == "cooperar" and opponent_decision == "cooperar":
         scores[player_id] += 2
         bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam 2 pontos!")
    elif player_decision == "cooperar" and opponent_decision == "trair":
         scores[player_id] -= 1
         bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu 1 ponto!")
    elif player_decision == "trair" and opponent_decision == "cooperar":
         scores[player_id] += 3
         bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou 3 pontos!")
    else:
         bot.send_message(player_id, "Você e seu oponente traíram. Ninguém ganhou pontos.")
    
    # Incrementar o número de rodadas
    round_number += 1
    
    # Enviar mensagens aos jogadores com os resultados da rodada
    bot.send_message(player_id, f"Na rodada {round_number}:\n\n"
                                f"Você jogou: {player_decision}\n"
                                f"O seu oponente jogou: {opponent_decision}\n"
                                f"Você recebeu uma sentença de {players[player_id]['sentenca']} anos\n"
                                f"Placar atual: {scores[player_id]} x {scores[opponent_id]}")
    bot.send_message(opponent_id, f"Na rodada {round_number}:\n\n"
                                   f"Você jogou: {opponent_decision}\n"
                                   f"O seu oponente jogou: {player_decision}\n"
                                   f"Você recebeu uma sentença de {players[opponent_id]['sentenca']} anos\n"
                                   f"Placar atual: {scores[opponent_id]} x {scores[player_id]}")
    
    # Limpar as decisões dos jogadores
    players[player_id]["decision"] = None
    players[opponent_id]["decision"] = None
    
    # Verificar se o jogo acabou
    if round_number >= 5:
        fim_de_jogo(player_id, opponent_id)

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

    
if __name__ == "__main__":
    bot.polling()
