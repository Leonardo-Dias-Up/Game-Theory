# %% Bibliotecas API e introdução

from random import choice, randint
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
acumulated_scores = {}

# Contador de rodadas
round_number = 0
opponent_decision = None

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
def jogar_contra_cpu(message):
    player_id = message.from_user.id

    global opponent_decision 
    
    opponent_decision = choice(["c", "t"])

    # Adiciona o jogador ao dicionário de jogadores
    players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}

    # Inicializa a pontuação do jogador em 0
    scores[player_id] = 0
    bot.send_message(player_id, "Digite 'c' para cooperar ou 't' para trair para fazer sua escolha.")

# Handler para o comando /pvp
@bot.message_handler(commands=['pvp'])
def jogar_pvp(message):
    
    global opponent_decision 
    
    try:
        opponent_id = players[player_id]["opponent_id"]
        opponent_decision = players[opponent_id]["decision"]
    except KeyError:
        bot.reply_to(message, "Você ainda não iniciou um jogo ou seu oponente ainda não fez sua jogada.")
        return
       
    player_id = message.from_user.id
    
    # Adiciona o jogador ao dicionário de jogadores
    players[player_id] = {"name": message.from_user.first_name, "decision": None, "opponent_id": player_id}

    # Inicializa a pontuação do jogador em 0
    scores[player_id] = 0
    bot.send_message(player_id, "Digite 'c' para cooperar ou 't' para trair para fazer sua escolha.")

@bot.message_handler(func=lambda message: message.text.lower() in ["c", "t"] and message.chat.id in players)
def jogada(message):
    player_id = message.from_user.id
    
    global opponent_id
    
    # Verifica se é a primeira jogada do jogador
    if player_id not in acumulated_scores:
        acumulated_scores[player_id] = 0
        
    # Armazena a escolha do jogador no dicionário de jogadores
    players[player_id]["decision"] = message.text.lower()
    
    # Envia mensagem de confirmação da jogada
    bot.send_message(player_id, f"Você escolheu {message.text.lower()}.")

    # Verifica se a jogada do oponente já foi feita
    opponent_id = players[player_id]["opponent_id"]
    if players[opponent_id]["decision"] is not None:
        player_decision = players[player_id]["decision"]
        
        if message.text.lower() == '/pvp':
            opponent_decision = players[opponent_id]["decision"]
        else:
            opponent_decision = choice(["c", "t"])
            opponent_id = 123987456  # Gera um id aleatório
        
        # Calcula a pontuação dos jogadores e atualiza o dicionário de pontuações
        if player_decision == "c" and opponent_decision == "c":
            scores[player_id] = [5]
            scores[opponent_id] = [5]
            acumulated_scores[player_id] += scores[player_id][0] 
            if opponent_id in acumulated_scores:
                acumulated_scores[opponent_id] += scores[opponent_id][0]
            else:
                acumulated_scores[opponent_id] = scores[opponent_id][0]
            bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam" + f" {scores[player_id]} pontos!")
        
        elif player_decision == "c" and opponent_decision == "t":
            scores[player_id] = [-10]
            scores[opponent_id] = [10]
            acumulated_scores[player_id] += scores[player_id][0] 
            if opponent_id in acumulated_scores:
                acumulated_scores[opponent_id] += scores[opponent_id][0]
            else:
                acumulated_scores[opponent_id] = scores[opponent_id][0]
            bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu" + f" {scores[player_id]} pontos!")
        
        elif player_decision == "t" and opponent_decision == "c":
            scores[player_id] = [10]
            scores[opponent_id] = [-10]
            acumulated_scores[player_id] += scores[player_id][0] 
            if opponent_id in acumulated_scores:
                acumulated_scores[opponent_id] += scores[opponent_id][0]
            else:
                acumulated_scores[opponent_id] = scores[opponent_id][0]
            bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou" + f" {scores[player_id]} pontos!")
        
        else:
            bot.send_message(player_id, "Você e seu oponente traíram. Ambos ganharam" + f" {scores[player_id]} pontos!")
            scores[player_id] = [1]
            scores[opponent_id] = [1]
            acumulated_scores[player_id] += scores[player_id][0] 
            if opponent_id in acumulated_scores:
                acumulated_scores[opponent_id] += scores[opponent_id][0]
            else:
                acumulated_scores[opponent_id] = scores[opponent_id][0] 
            
        # Envia mensagem com as pontuações atuais dos jogadores e remove os jogadores do dicionário de jogadores
        bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}\nPontuação do oponente: {scores[opponent_id]}")
        bot.send_message(player_id, f"Sua pontuação acumulada: {acumulated_scores[player_id]}\nPontuação acumulada do oponente: {acumulated_scores[opponent_id]}")
        bot.send_message(player_id, "Digite /pvp para jogar novamente contra um jogador ou /cpu para jogar contra o computador ou digite qualquer outra coisa para sair.")
        players.pop(player_id)
        
        try:
            players.pop(opponent_id)
        except:
            pass
    else:
        # Envia mensagem para o oponente fazer sua jogada
        bot.send_message(opponent_id, f"O seu oponente jogou: {message.text.lower()}\nAgora é a sua vez de jogar!")

# %%
import sqlite3

# SQLite connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                is_available BOOLEAN DEFAULT 0)''')


# Handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name

    # Check if user already exists in database
    cursor.execute("SELECT * FROM users WHERE id = ?", (chat_id,))
    user = cursor.fetchone()

    if not user:
        # If user doesn't exist, insert new record into database
        cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (chat_id, first_name))
        conn.commit()

    # Send welcome message
    bot.send_message(chat_id, f"Olá, {first_name}! Use os comandos para gerenciar sua disponibilidade.")


# Handler for /disponivel command
@bot.message_handler(commands=['disponivel'])
def set_available(message):
    chat_id = message.chat.id

    # Update user availability
    cursor.execute("UPDATE users SET is_available = ? WHERE id = ?", (True, chat_id))
    conn.commit()

    # Send confirmation message
    bot.send_message(chat_id, "Sua disponibilidade foi atualizada para 'disponível'.")


# Handler for /indisponivel command
@bot.message_handler(commands=['indisponivel'])
def set_unavailable(message):
    chat_id = message.chat.id

    # Update user availability
    cursor.execute("UPDATE users SET is_available = ? WHERE id = ?", (False, chat_id))
    conn.commit()

    # Send confirmation message
    bot.send_message(chat_id, "Sua disponibilidade foi atualizada para 'indisponível'.")


# Handler for /listar command
@bot.message_handler(commands=['listar'])
def list_users(message):
    chat_id = message.chat.id

    # Get list of all users and their availability
    cursor.execute("SELECT name, is_available FROM users")
    users = cursor.fetchall()

    if not users:
        bot.send_message(chat_id, "Nenhum usuário cadastrado.")
    else:
        # Format list of users as a string
        users_str = ""
        for user in users:
            status = "Disponível" if user[1] else "Indisponível"
            users_str += f"{user[0]} - {status}\n"

        # Send list of users as a message
        bot.send_message(chat_id, users_str)
    
if __name__ == "__main__":
    bot.polling()