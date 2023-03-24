import random
import telebot

bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.decision = None
        self.opponent = None
        self.score = 0

    def play(self, decision):
        self.decision = decision
        if self.opponent.decision is not None:
            self.update_scores()

    def update_scores(self):
        if self.decision == "cooperar" and self.opponent.decision == "cooperar":
            self.score += 2
            self.opponent.score += 2
        elif self.decision == "cooperar" and self.opponent.decision == "trair":
            self.score -= 1
            self.opponent.score += 3
        elif self.decision == "trair" and self.opponent.decision == "cooperar":
            self.score += 3
            self.opponent.score -= 1
        else:
            pass  # both players betray, no one gets points

        bot.send_message(self.id, f"Você jogou: {self.decision}")
        bot.send_message(self.id, f"{self.opponent.name} jogou: {self.opponent.decision}")
        bot.send_message(self.id, f"Sua pontuação atual: {self.score}")
        bot.send_message(self.opponent.id, f"Você jogou: {self.opponent.decision}")
        bot.send_message(self.opponent.id, f"{self.name} jogou: {self.decision}")
        bot.send_message(self.opponent.id, f"Sua pontuação atual: {self.opponent.score}")

        self.decision = None
        self.opponent.decision = None
        self.opponent = None

players = []
game_mode = None

@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Bem-vindo ao jogo do dilema dos prisioneiros!\n\n" \
           "O objetivo do jogo é maximizar sua pontuação ao cooperar ou trair seu oponente. Cada jogador deve escolher 'cooperar' ou 'trair'.\n\n" \
           "Digite 'cooperar' ou 'trair' para jogar. Você pode jogar contra outros jogadores ou contra a máquina. Para jogar contra a máquina, digite /cpu. Para jogar contra outros jogadores, digite /multiplayer."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['cpu'])
def play_vs_cpu(message):
    global game_mode
    game_mode = "cpu"

    player = Player(message.chat.id, message.from_user.first_name)
    players.append(player)

    bot.send_message(player.id, "Você escolheu jogar contra a máquina. Digite 'cooperar' ou 'trair' para jogar.")

    while player.decision is None:
        pass

    if player.decision == "cooperar":
        cpu_decision = "trair"
    else:
        cpu_decision = random.choice(["cooperar", "trair"])

    player.opponent = Player(0, "CPU")
    player.opponent.decision = cpu_decision
    player.play(player.decision)

    bot.send_message(player.id, f"A CPU jogou: {cpu_decision}")
    bot.send_message(player.id, f"Sua pontuação atual: {player.score}")

@bot.message_handler(commands=['multiplayer'])
def play_multiplayer(message):
    global game_mode
    game_mode = "multiplayer"
    player = Player(message.chat.id, message.from_user.first_name)
    players.append(player)

    bot.send_message(player.id, "Você escolheu jogar contra outros jogadores. Aguardando mais jogadores para iniciar o jogo...")

    if len(players) == 2:
        players[0].opponent = players[1]
        players[1].opponent = players[0]

        bot.send_message(players[0].id, f"Jogo iniciado contra {players[1].name}!")
        bot.send_message(players[1].id, f"Jogo iniciado contra {players[0].name}!")

        bot.send_message(players[0].id, "Digite 'cooperar' ou 'trair' para jogar!")
        bot.send_message(players[1].id, "Digite 'cooperar' ou 'trair' para jogar!")

def get_player(player_id):
    for player in players:
        if player.id == player_id:
            return player
    return None

@bot.message_handler(func=lambda message: message.text in ['cooperar', 'trair'])
def play_game(message):
    player = get_player(message.chat.id)

    if player is None:
        bot.send_message(message.chat.id, "Você ainda não iniciou um jogo. Digite /start para começar.")

    elif game_mode == "cpu":
        cpu_decision = random.choice(['cooperar', 'trair'])
        player.opponent = Player(None, "Máquina")
        player.opponent.play(cpu_decision)
        player.play(message.text)
        player.update_scores()

    elif player.opponent is None:
        bot.send_message(message.chat.id, "Aguardando outro jogador para iniciar o jogo...")

    else:
        player.play(message.text)
        if player.opponent.decision is not None:
            player.update_scores()
            if len(players) == 2:
                bot.send_message(player.id, "Aguardando jogada de seu oponente...")
                bot.send_message(player.opponent.id, "Sua vez de jogar!")

    if player is not None and player.opponent is not None and player.opponent.decision is None:
        bot.send_message(player.opponent.id, "Aguardando jogada de seu oponente...")
        bot.send_message(player.id, "Sua vez de jogar!")
        
if __name__ == "__main__":
    bot.polling()