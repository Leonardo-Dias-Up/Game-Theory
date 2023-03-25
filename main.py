# %% Bibliotecas API e introdução

from random import choice, randint
import telebot   
from random import sample
import sqlite3
import threading

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
       
# Conectar ao banco de dados
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Criação da tabela de jogadores
c.execute("""
    CREATE TABLE IF NOT EXISTS jogadores (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        sobrenome TEXT,
        disponivel INTEGER
    )
""")
conn.commit()

# Função para buscar jogadores disponíveis no banco de dados
def buscar_jogadores_disponiveis():
    c.execute("SELECT id, nome, sobrenome FROM jogadores WHERE disponivel = 1")
    jogadores = c.fetchall()
    return jogadores

# Função para atualizar o status de disponibilidade do jogador no banco de dados
def atualizar_disponibilidade_jogador(jogador_id, disponivel):
    c.execute("UPDATE jogadores SET disponivel = ? WHERE id = ?", (disponivel, jogador_id))
    conn.commit()
    
# Mensagem de boas-vindas
def welcome_message(message):
    text = "Bem-vindo ao jogo do dilema dos prisioneiros!\n\n" \
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu. Para jogar contra outros jogadores, digite /multiplayer." \
            "Para jogar, você precisa estar disponível para isso basta clicar em /register \
            e seguir preencher seu nome para o jogo." \
            "Ao usar o comando /multiplayer, você será pareado com outro jogador " \
            "disponível no momento. Para ficar indisponível, use o comando /close."
            
    bot.send_message(message.chat.id, text)
    
# Handler para o comando /start
@bot.message_handler(commands=['start'])
def start_message(message):
    jogador_id = message.chat.id
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jogadores WHERE id=?", (jogador_id,))
    row = c.fetchone()
    jogador_nome = ""
    if row is None:
        c.execute("INSERT INTO jogadores (id, nome, disponivel) VALUES (?, ?, ?)", (jogador_id, message.chat.first_name, 'INICIO'))
        conn.commit()
        bot.reply_to(message, "Bem-vindo ao jogo!")
    else:
        jogador_nome = row[1]
    bot.reply_to(message, "Bem-vindo, " + jogador_nome + "! Você está disponível para jogar!")
    conn.close()        
            
    # Imprime o menu com a descrição do jogo
    welcome_message(message)

# Handler para o comando /register
@bot.message_handler(commands=['register'])
def register_message(message):
    # Envia uma mensagem de boas-vindas e instruções para o jogador
    bot.send_message(message.chat.id, "Bem-vindo ao jogo! Por favor, preencha o formulário de cadastro com as seguintes informações:")
    bot.send_message(message.chat.id, "Nome:")
    
    # Adiciona o jogador à lista de jogadores aguardando cadastro
    jogadores_aguardando_cadastro.append(message.chat.id)

# Handler para receber as informações de cadastro
@bot.message_handler(func=lambda message: message.chat.id in jogadores_aguardando_cadastro)
def receive_registration_info(message):
    jogador_id = message.chat.id
    jogador_nome = message.text
    
    # Atualiza o nome do jogador no banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE jogadores SET nome = ?, disponivel = ? WHERE id = ?", (jogador_nome, 1, jogador_id))
    conn.commit()
    conn.close()
    
    # Remove o jogador da lista de jogadores aguardando cadastro
    jogadores_aguardando_cadastro.remove(jogador_id)
    
    # Envia uma mensagem de confirmação ao jogador
    bot.send_message(jogador_id, "Cadastro realizado com sucesso! Agora você está disponível para jogar.")

# Registra novos usuário para o pareamento
@bot.message_handler(commands=['register'])
def register_message(message):
    jogador_id = message.chat.id
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jogadores WHERE id=?", (jogador_id,))
    row = c.fetchone()
    if row is None:
        jogadores_aguardando_cadastro.append(jogador_id)
        bot.reply_to(message, "Digite o seu nome completo para se cadastrar.")
    else:
        bot.reply_to(message, "Você já está cadastrado. Use o comando /disponivel para ficar disponível para jogar.")
    conn.close()
    buscar_jogadores_disponiveis()

# Lista de jogadores aguardando cadastro
jogadores_aguardando_cadastro = []

# Handler para receber as informações de cadastro
@bot.message_handler(func=lambda message: message.chat.id in jogadores_aguardando_cadastro)
def receive_registration_info(message):
    jogador_id = message.chat.id
    jogador_nome = message.text
    
    # Atualiza o nome do jogador no banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE jogadores SET nome = ?, disponivel = ? WHERE id = ?", (jogador_nome, 1, jogador_id))
    conn.commit()
    conn.close()
    
    # Remove o jogador da lista de jogadores aguardando cadastro
    jogadores_aguardando_cadastro.remove(jogador_id)
    
    # Envia uma mensagem de confirmação ao jogador
    bot.send_message(jogador_id, "Cadastro realizado com sucesso! Agora você está disponível para jogar.")

# Handler para o comando /close
@bot.message_handler(commands=['close'])
def close_message(message):
    
    # Remover a disponibilidade do jogador no banco de dados
    jogador_id = message.from_user.id
    
    c.execute("UPDATE jogadores SET disponivel = 0 WHERE id = ?", (jogador_id,))
    
    conn.commit()
    
    bot.reply_to(message, "Você não está mais disponível para jogar.")

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
                    bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam 1 pontos!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou /close para finalizar, caso queria jogar pvp /multiplayer ou /start.")
                    players.pop(player_id)
                    
                elif player_decision == "cooperar" and opponent_decision == "trair":
                    scores[player_id] -= 1
                    
                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu -10 ponto!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou /close para finalizar, caso queria jogar pvp /multiplayer ou /start.")
                    players.pop(player_id)
                    
                elif player_decision == "trair" and opponent_decision == "cooperar":
                    scores[player_id] += 3

                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou 10 pontos!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou /close para finalizar, caso queria jogar pvp /multiplayer ou /start.")
                    players.pop(player_id)
                    
                else:                  
                    # Respostas das escolhas tomadas pelos jogadores
                    bot.send_message(player_id, f"Sua escolha: {player_decision}")
                    bot.send_message(player_id, f"O seu oponente jogou: {opponent_decision}")
                    bot.send_message(player_id, f"Sua pontuação atual: {scores[player_id]}")
                    bot.send_message(player_id, "Você e seu oponente traíram. Você ganhou 1 pontos!")
                    bot.send_message(player_id, "Digite /cpu para jogar novamente contra o computador ou /close para finalizar, caso queria jogar pvp /multiplayer ou /start.")
                    players.pop(player_id)
                   
        else:
            multiplayer_message(message) # chama a função multiplayer
            
# Função para o fim do jogo
def fim_de_jogo(player_id, opponent_id):
    global round_number, scores, players
    
    # Reiniciar as variáveis do jogo
    round_number = 0
    scores = {player_id: 0, opponent_id: 0}
    players = {player_id: {"decision": None, "sentenca": randint(1, 10)}, 
               opponent_id: {"decision": None, "sentenca": randint(1, 10)}}
    
    # Enviar mensagem de fim de jogo
    bot.send_message(player_id, "O jogo acabou. Reiniciando...")
    bot.send_message(opponent_id, "O jogo acabou. Reiniciando...")


# Inicio do jogo 
def iniciar_jogo(player_id, opponent_id, player_decision):
    global round_number
    
    # Verifica se a jogada do oponente já foi feita
    opponent_decision = players[opponent_id]["decision"]
    
    # Verificar as decisões de ambos os jogadores
    if player_decision == "cooperar" and opponent_decision == "cooperar":
         scores[player_id] += 2
         bot.send_message(player_id, "Você e seu oponente cooperaram. Ambos ganharam 1 pontos!")
    elif player_decision == "cooperar" and opponent_decision == "trair":
         scores[player_id] -= 1
         bot.send_message(player_id, "Você cooperou, mas seu oponente traiu. Você perdeu -10 ponto!")
    elif player_decision == "trair" and opponent_decision == "cooperar":
         scores[player_id] += 3
         bot.send_message(player_id, "Você traiu, mas seu oponente cooperou. Você ganhou 10 pontos!")
    else:
         bot.send_message(player_id, "Você e seu oponente traíram. Ninguém ganhou pontos. Você ganhou 5 pontos!")
    
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
    if scores[player_id] >= 10:
        bot.send_message(player_id, "Você atingiu a pontuação máxima de 10 pontos. Parabéns, você venceu!")
        bot.send_message(opponent_id, "Seu oponente atingiu a pontuação máxima de 10 pontos. Infelizmente, você perdeu.")
        fim_de_jogo(player_id, opponent_id)
    elif scores[opponent_id] >= 10:
        bot.send_message(opponent_id, "Você atingiu a pontuação máxima de 10 pontos. Parabéns, você venceu!")
        bot.send_message(player_id, "Seu oponente atingiu a pontuação máxima de 10 pontos. Infelizmente, você perdeu.")
        fim_de_jogo(player_id, opponent_id)
    else:
        # Se o jogo não acabou, iniciar a próxima rodada
        iniciar_rodada(player_id, opponent_id)

def iniciar_rodada(player_id, opponent_id):
    # Verificar se ambos os jogadores já fizeram sua jogada
    player_decision = players[player_id]["decision"]
    opponent_decision = players[opponent_id]["decision"]
    
    if player_decision is None or opponent_decision is None:
        return
    
    # Iniciar a jogada
    iniciar_jogo(player_id, opponent_id, player_decision)

# Define um dicionário para armazenar as salas de jogo
game_rooms = {}

# Handler para o comando /multiplayer
# Handler para o comando /multiplayer
@bot.message_handler(commands=['multiplayer'])
def jogar_multiplayer_mensagem(message):
    multiplayer_matchmaking(message)
    player_id = message.from_user.id
    
    if player_id not in game_rooms:
        # Adiciona o jogador a uma nova sala de jogo
        add_player_to_game_room(player_id)
    else:
        bot.send_message(player_id, "Você já está na sala de jogo. Aguarde um adversário.")

# Handler para as mensagens enviadas pelos jogadores na sala de jogo
@bot.message_handler(func=lambda message: True)
def jogar_contra_jogador(message):
    player_id = message.from_user.id

    # Verifica se o jogador está em uma sala de jogo
    if player_id in game_rooms:
        opponent_id = game_rooms[player_id]["opponent_id"]

        # Verifica se o jogador tem um adversário na sala de jogo
        if opponent_id is not None:
            # Encaminha a mensagem do jogador para o seu adversário
            bot.send_message(opponent_id, f"{game_rooms[player_id]['name']}: {message.text}")
        else:
            bot.send_message(player_id, "Aguarde um adversário.")
    else:
        multiplayer_message(message) # chama a função multiplayer

# Função para adicionar um jogador a uma sala de jogo
def add_player_to_game_room(player_id):
    global game_rooms

    # Verifica se há uma sala de jogo com um jogador aguardando adversário
    waiting_rooms = [room for room in game_rooms.values() if room["opponent_id"] is None]

    if waiting_rooms:
        # Escolhe aleatoriamente uma sala de jogo com um jogador aguardando adversário
        room = choice(waiting_rooms)

        # Adiciona o jogador à sala de jogo selecionada
        room["opponent_id"] = player_id
        game_rooms[player_id] = {"name": room["name"], "decision": None, "opponent_id": room["opponent_id"]}

        # Notifica ambos os jogadores da sala de jogo
        bot.send_message(room["opponent_id"], "Adversário encontrado. O jogo começará em breve.")
        bot.send_message(player_id, "Adversário encontrado. O jogo começará em breve.")
    else:
        # Cria uma nova sala de jogo com o jogador aguardando adversário
        game_rooms[player_id] = {"name": None, "decision": None, "opponent_id": None}
        bot.send_message(player_id, "Você foi adicionado à sala de jogo. Aguarde um adversário.")

def multiplayer_message(message):
    bot.send_message(message.chat.id, "Para jogar multiplayer, digite /multiplayer. Você será adicionado a uma sala de jogo e aguardará por um adversário.")


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