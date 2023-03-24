import telebot
from random import choice
from random import randint
from random import choice

CHAVE_API_TELEGRAM = "5570452334:AAHmIZApvbKb1wd8hSiOj6BKu6-TNMINd-8"

bot = telebot.TeleBot(CHAVE_API_TELEGRAM)

user = bot.get_me()
updates = bot.get_updates()

players = {}
scores = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Olá, bem-vindo ao jogo de cooperação! Digite /cpu para jogar contra o computador ou /multiplayer para jogar contra outro jogador.")

# Função para o comando /cpu
@bot.message_handler(commands=['cpu'])
def jogar_so_mensagem(message):
    player_id = message.from_user.id

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}
        scores[player_id] = 0
        bot.send_message(player_id, "Você está jogando contra si mesmo!")
        bot.send_message(player_id, "Digite 'cooperar' ou 'trair': ")
    else:
        bot.send_message(player_id, "Você já está jogando uma partida! Digite 'desistir' para sair do jogo.")

# Função para o comando /multiplayer
@bot.message_handler(commands=['multiplayer'])
def jogar_multiplayer_mensagem(message):
    player_id = message.from_user.id

    if player_id not in players:
        players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": None}
        scores[player_id] = 0
        bot.send_message(player_id, "Você está aguardando um adversário para jogar. Aguarde...")
        procurar_adversario(player_id)
    else:
        bot.send_message(player_id, "Você já está jogando uma partida! Digite 'desistir' para sair do jogo.")

# Função para procurar adversário
def procurar_adversario(player_id):
    players_sem_adversario = [player for player in players if players[player]["opponent_id"] is None and player != player_id]

    if len(players_sem_adversario) > 0:
        # Escolhe um jogador aleatório que não esteja jogando contra ninguém
        opponent_id = choice(players_sem_adversario)
        players[player_id]["opponent_id"] = opponent_id
        players[opponent_id]["opponent_id"] = player_id
        bot.send_message(player_id, f"Seu adversário é {players[opponent_id]['name']}.")
        bot.send_message(opponent_id, f"Seu adversário é {players[player_id]['name']}.")
        bot.send_message(player_id, "Digite 'cooperar' ou 'trair': ")
        bot.send_message(opponent_id, "Digite 'cooperar' ou 'trair': ")
    else:
        bot.send_message(player_id, "Ainda não há adversários disponíveis. Aguarde...")

# Função para jogar uma partida contra a máquina
def jogar_so(player_id, decision):
    opponent_decision = choice(["cooperar", "trair"])
    players[player_id]["decision"] = decision
    players[player_id]["opponent_decision"] = opponent_decision

    if decision == "cooperar" and opponent_decision == "cooperar":
        bot.send_message(player_id, "Ambos cooperaram. +2 pontos!")
        scores[player_id] += 2
    elif decision == "cooperar" and opponent_decision == "trair":
        bot.send_message(player_id, "Você cooperou e seu adversário traiu. -1 ponto!")
        scores[player_id] -= 1
    elif decision == "trair" and opponent_decision == "cooperar":
        bot.send_message(player_id, "Você traiu e seu adversário cooperou. +3 pontos!")
        scores[player_id] += 3
    elif decision == "trair" and opponent_decision == "trair":
        bot.send_message(player_id, "Ambos traíram. 0 pontos.")
        jogar_novamente(player_id)

#Função para jogar uma partida multiplayer
def jogar_multiplayer(player_id, decision):
    opponent_id = players[player_id]["opponent_id"]
    players[player_id]["decision"] = decision
    
    # Aguarda a jogada do adversário
    while players[opponent_id]["decision"] is None:
        pass

    opponent_decision = players[opponent_id]["decision"]
    players[player_id]["opponent_decision"] = opponent_decision

    if decision == "cooperar" and opponent_decision == "cooperar":
        bot.send_message(player_id, "Ambos cooperaram. +2 pontos!")
        scores[player_id] += 2
        scores[opponent_id] += 2
    elif decision == "cooperar" and opponent_decision == "trair":
        bot.send_message(player_id, "Você cooperou e seu adversário traiu. -1 ponto!")
        scores[player_id] -= 1
        scores[opponent_id] += 3
    elif decision == "trair" and opponent_decision == "cooperar":
        bot.send_message(player_id, "Você traiu e seu adversário cooperou. +3 pontos!")
        scores[player_id] += 3
        scores[opponent_id] -= 1
    elif decision == "trair" and opponent_decision == "trair":
        bot.send_message(player_id, "Ambos traíram. 0 pontos.")
    jogar_novamente_multiplayer(player_id)

#Função para jogar novamente contra a máquina
def jogar_novamente(player_id):
    bot.send_message(player_id, "Você quer jogar novamente? (sim/não)")
    players[player_id]["opponent_decision"] = None
    
#Função para jogar novamente multiplayer
def jogar_novamente_multiplayer(player_id):
    bot.send_message(player_id, "Você quer jogar novamente? (sim/não)")
    opponent_id = players[player_id]["opponent_id"]
    players[player_id]["opponent_decision"] = None
    players[opponent_id]["decision"] = None

#Função para sair da partida
def sair(player_id):
    if player_id in players:
        opponent_id = players[player_id]["opponent_id"]
    if opponent_id is not None:
        bot.send_message(opponent_id, "Seu adversário desistiu.")
        players[opponent_id]["opponent_id"] = None
        scores[opponent_id] = 0
        players.pop(player_id)
        scores.pop(player_id)

#Função para verificar a mensagem enviada pelo usuário
@bot.message_handler(func=lambda message: True)
def verificar_mensagem(message):
    player_id = message.from_user.id
    if message.text.lower() == "cooperar":
        if player_id in players and players[player_id]["opponent_id"] is not None:
            jogar_multiplayer(player_id, "cooperar")
        else:
            jogar_so(player_id, "cooperar")
    elif message.text.lower() == "trair":
        if player_id in players and players[player_id]["opponent_id"] is not None:
            jogar_multiplayer(player_id, "trair")
        else:
            jogar_so(player_id, "trair")


if __name__ == "__main__":
    bot.polling()
