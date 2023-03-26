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
    player_id = message.from_user.id
    
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
            scores[player_id] = [1]
            scores[opponent_id] = [1]
            bot.send_message(player_id, "Você e seu oponente traíram. Ambos ganharam" + f" {scores[player_id]} pontos!")
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
conn = sqlite3.connect('database.db', check_same_thread=False)

cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                is_available BOOLEAN DEFAULT 0)''')


# Handler for /begin command
@bot.message_handler(commands=['begin'])
def start(message):
    chat_id = message.chat.id
    
    # Ask the user for their name
    bot.reply_to(message, "Olá! Qual o seu nome?")
    
    # Register a handler for the next message from the user, which will handle the name
    bot.register_next_step_handler(message, save_name, chat_id)
    
def save_name(message, chat_id):
    name = message.text
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (id, name, is_available) VALUES (?, ?, ?)", (chat_id, name, 0))
        cursor.connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    bot.reply_to(message, f"Seja bem vindo {name} ao jogo Dilema dos Prisioneiros!")

# set_available command
@bot.message_handler(commands=['set_available'])
def set_available(message):
    chat_id = message.chat.id
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE users SET is_available = ? WHERE id = ?", (1, chat_id))
        cursor.connection.commit()
        bot.reply_to(message, "Você está disponível agora!")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Ocorreu um erro ao tentar atualizar sua disponibilidade. Tente novamente mais tarde.")
    finally:
        cursor.close()
        conn.close()

# get_users command
@bot.message_handler(commands=['get_users'])
def get_users(message):
    chat_id = message.chat.id
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        users = []
        for row in cursor.execute("SELECT * FROM users"):
            users.append(row[1])

        bot.reply_to(message, f"Usuários cadastrados: {', '.join(users)}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # update user availability
        cursor.execute("UPDATE users SET is_available = ? WHERE id = ?", (1, chat_id))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        
    bot.reply_to(message, "Você está agora disponível!")

# set_unavailable command
@bot.message_handler(commands=['set_unavailable'])
def set_unavailable(message):
    chat_id = message.chat.id

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # update user availability
        cursor.execute("UPDATE users SET is_available = ? WHERE id = ?", (0, chat_id))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    bot.reply_to(message, "Você não está mais disponível.")

# get_users command
@bot.message_handler(commands=['get_users'])
def get_users(message):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        users = []
        for row in cursor.execute("SELECT * FROM users"):
            users.append(row[1])

        bot.reply_to(message, f"Usuários cadastrados: {', '.join(users)}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    bot.reply_to(message, f"Usuários cadastrados: {', '.join(users)}")

# close connection and cursor
cursor.close()
conn.close()


# %%
"""
    # Cria conexão com o banco de dados
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cria tabela questions
cursor.execute('''CREATE TABLE questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, option1 TEXT, option2 TEXT)''')

# Insere a pergunta na tabela questions
cursor.execute("INSERT INTO questions (text, option1, option2) VALUES ('Cooperar ou trair?', 'Cooperar', 'Trair')")

# Fecha a conexão com o banco de dados
conn.commit()
cursor.close()
conn.close()
"""

"""
import sqlite3
import schedule
import time

# Cria conexão com o banco de dados
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Função para verificar se há dois usuários disponíveis e enviar a pergunta
def send_question():
    # Verifica se há dois usuários disponíveis
    cursor.execute("SELECT * FROM users WHERE is_available=1 LIMIT 2")
    users = cursor.fetchall()
    if len(users) == 2:
        # Seleciona a pergunta aleatória
        cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        question, option1, option2 = cursor.fetchone()[1:]
        
        # Envia a pergunta para os usuários
        for user in users:
            message = f'{question}\n\n1. {option1}\n2. {option2}'
            send_message(user[0], message)  # Envia a mensagem para o usuário
            cursor.execute("UPDATE users SET is_available=0 WHERE id=?", (user[0],))
        
        # Insere a pergunta na tabela game_results
        cursor.execute("INSERT INTO game_results (player1_id, player2_id, question_id) VALUES (?, ?, ?)", (users[0][0], users[1][0], question_id))
        conn.commit()

# Agendando a execução da função de verificação a cada 10 segundos
schedule.every(10).seconds.do(send_question)

# Loop infinito para executar as tarefas agendadas
while True:
    schedule.run_pending()
    time.sleep(1)
    
"""

"""
def play_game(player1_id, player2_id, question_id):
    # Envia a pergunta para os jogadores
    message = f"{question}\n\n1. {option1}\n2. {option2}"
    send_message(player1_id, message)
    send_message(player2_id, message)

    # Aguarda as respostas dos jogadores
    player1_choice = receive_message(player1_id)
    player2_choice = receive_message(player2_id)

    # Grava as respostas no banco de dados
    cursor.execute(f"INSERT INTO game_results (player1_id, player2_id, question_id, player1_choice, player2_choice) VALUES ({player1_id}, {player2_id}, {question_id}, {player1_choice}, {player2_choice})")
    conn.commit()

    # Determina o resultado do jogo
    if player1_choice == 1 and player2_choice == 1:
        result = "Os dois jogadores cooperaram."
    elif player1_choice == 1 and player2_choice == 2:
        result = "O jogador 1 cooperou e o jogador 2 traiu."
    elif player1_choice == 2 and player2_choice == 1:
        result = "O jogador 1 traiu e o jogador 2 cooperou."
    else:
        result = "Os dois jogadores traíram."

    # Atualiza o registro no banco de dados com o resultado
    cursor.execute(f"UPDATE game_results SET result = '{result}' WHERE player1_id = {player1_id} AND player2_id = {player2_id} AND question_id = {question_id}")
    conn.commit()

    # Envia o resultado para os jogadores
    send_message(player1_id, result)
    send_message(player2_id, result)

"""
if __name__ == "__main__":
    bot.polling()