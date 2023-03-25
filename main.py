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
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu."
    bot.send_message(message.chat.id, text)
    
# Handler para o comando /start
@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message(message)

# Handler para o comando /cpu
@bot.message_handler(commands=['cpu'])

# Envia mensagem para o jogador escolher sua jogada
def jogar_contra_cpu(message):
    
    if message.text == '/cpu':
        player_id = message.from_user.id
        
    player_id = message.from_user.id
    
    # Handler para o comando /cpu
    players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
    
    # Inicializa a pontuação do jogador em 0
    scores[player_id] = 0
    bot.send_message(player_id, "Digite 'cooperar' ou 'trair' para fazer sua escolha.")
    
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
            bot.send_message("Obrigado por Jogar")

   
if __name__ == "__main__":
    bot.polling()
