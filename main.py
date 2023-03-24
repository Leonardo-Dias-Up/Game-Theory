# %% Bibliotecas API e introdução

from random import choice
import telebot   
from random import sample

# Chave da API do Telegram
CHAVE_API_TELEGRAM = "5570452334:AAHmIZApvbKb1wd8hSiOj6BKu6-TNMINd-8"

# Criação do objeto bot
bot = telebot.TeleBot(CHAVE_API_TELEGRAM)
user = bot.get_me()
updates = bot.get_updates()

# Dicionários para armazenar os jogadores e pontuações
players = {}
scores = {}

# Contador de rodadas
round_number = 0

# Dicionário para armazenar os jogadores disponíveis para jogo multiplayer
jogadores_disponiveis = {}

# Função que descreve os desenvolvedores do jogo
def describe_project(message):
    text = "Desenvolvedores: Leonardo Dias e Djalma. 2023"
    bot.send_message(message.chat.id, text)

# Handler para o comando /help
@bot.message_handler(commands=['help'])
def help_message(message):
    describe_project(message)
    
# Mensagem de boas-vindas
def welcome_message(message):
    text = "Bem-vindo ao jogo do dilema dos prisioneiros!\n\n" \
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu. Para jogar contra outros jogadores, digite /multiplayer."
    bot.send_message(message.chat.id, text)
    
# Handler para o comando /start
@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message(message)

# Handler para o comando /cpu
@bot.message_handler(commands=['cpu'])
def jogar_cpu_ou_so_mensagem(message):
    if message.text == '/cpu':
        player_id = message.from_user.id

    if player_id not in players:
         
        # Handler para o comando /cpu
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
        
        # Inicializa a pontuação do jogador em 0
        scores[player_id] = 0
        
        # Envia mensagem para o jogador escolher sua jogada
        bot.send_message(player_id, "Digite 'cooperar' ou 'trair' para fazer sua escolha.")
    else:
        bot.send_message(player_id, "Você já está jogando contra si mesmo!")

# Envia mensagem para o jogador escolher sua jogada
@bot.message_handler(func=lambda message: True)
def jogar_contra_cpu(message):
    player_id = message.from_user.id

    # Envia mensagem para o jogador escolher sua jogada
    if player_id in players:
        opponent_id = players[player_id]["opponent_id"]
        if message.text.lower() in ["cooperar", "trair"]:
            players[player_id]["decision"] = message.text.lower()

            # Verifica se a jogada do oponente já foi feita
            if players[opponent_id]["decision"] is not None:
                player_decision = players[player_id]["decision"]
                
                # Verifica se a jogada do oponente já foi feita
                opponent_decision = choice(["cooperar", "trair"])
                
                # Armazena a jogada do oponente no dicionário de jogadores
                players[player_id]["opponent_decision"] = opponent_decision
                bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                
               # Verificar as decisões de ambos os jogadores
                if player_decision == "cooperar" and opponent_decision == "cooperar":
                    scores[player_id] += 2
                    
                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam 2 pontos!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou digite qualquer outra coisa para sair.")
                    players.pop(player_id)
                    
                elif player_decision == "cooperar" and opponent_decision == "trair":
                    scores[player_id] -= 1
                    
                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu 1 ponto!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou digite qualquer outra coisa para sair.")
                    players.pop(player_id)
                    
                elif player_decision == "trair" and opponent_decision == "cooperar":
                    scores[player_id] += 3

                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou 3 pontos!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou digite qualquer outra coisa para sair.")
                    players.pop(player_id)
                    
                else:                  
                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você e seu oponente traíram. Ninguém ganhou pontos.")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou digite qualquer outra coisa para sair.")
                    players.pop(player_id)
                   
        else:
            multiplayer_message(message) # chama a função multiplayer

# Encerramento do jogo 
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

# Inicio do jogo 
def iniciar_jogo(player_id, opponent_id, player_decision):
    global round_number
    
    # Verifica se a jogada do oponente já foi feita
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

# Handler para o comando /multiplayer
@bot.message_handler(commands=['multiplayer'])

# Inicio do jogo para multiplayer
def multiplayer_message(message):
    jogador1 = None
    if len(jogadores_disponiveis) < 2:
        bot.send_message(message.chat.id, "Desculpe, não há jogadores suficientes disponíveis no momento.")
    else:
        # Escolher dois jogadores aleatoriamente
        jogador1, jogador2 = sample(jogadores_disponiveis, k=2)
        players[jogador1]["opponent_id"] = jogador2
        players[jogador2]["opponent_id"] = jogador1

        bot.send_message(jogador1, "Você está jogando contra " + players[jogador2]["name"])
       
    # Encerrar o jogo e enviar a pontuação final
    if jogador1 is not None:
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

# Handler para o comando /pontuacao
@bot.message_handler(commands=['pontuacao'])
def pontuacao_message(message):
    text = "Pontuações:\n\n"
    for player_id, score in scores.items():
        player_name = players[player_id]["name"]
        text += f"{player_name}: {score}\n"
    bot.send_message(message.chat.id, text)

    
if __name__ == "__main__":
    bot.polling()