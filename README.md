# Game-Theory
 Teoria dos jogos - Aplicações

bot/
├── bot/
│   ├── migrations/
│   │   └── ...
│   ├── templates/
│   │   └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   └── views.py
├── static/
│   └── ...
├── media/
│   └── ...
├── theory_game/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
├── mysite/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt


O código é um jogo chamado "Dilema dos prisioneiros" que é implementado no aplicativo de mensagens do Telegram usando a biblioteca Telebot. No jogo, os jogadores escolhem entre cooperar ou trair para obter uma pontuação, que é calculada com base nas escolhas feitas por ambos os jogadores.

O jogo começa com os jogadores enviando a mensagem "/start" para o bot para se inscreverem. Se houver apenas um jogador, ele terá que esperar até que outro jogador se inscreva para poder jogar. O jogo pode ser jogado sozinho usando o comando "/cpu".

O bot mantém um dicionário "players" para armazenar informações sobre os jogadores, como seu nome, decisão e id do oponente. Um dicionário "scores" é usado para manter a pontuação dos jogadores. O número de rodadas é rastreado por uma variável global "round_number".

Quando um jogador envia uma mensagem, a função "handle_message" é chamada, que verifica se o jogador está inscrito no jogo e se já tomou uma decisão. Se o jogador ainda não se inscreveu no jogo, o bot pede que ele se inscreva usando "/start". Se o jogador não tomou uma decisão, o bot pede que ele escolha entre "cooperar" ou "trair". Se o jogador tomou uma decisão e seu oponente também tomou uma decisão, as pontuações são calculadas com base nas escolhas dos jogadores.

Quando um novo jogador se inscreve, a função "jogo" é chamada, que adiciona o jogador à lista de jogadores e espera por outro jogador. Quando outro jogador se inscreve, os jogadores são emparelhados e o jogo começa via comando "/multiplayer". Se um jogador usar o comando "/cpu", o jogo começa com o jogador jogando contra si mesmo.

O bot envia mensagens aos jogadores informando-os sobre o resultado do jogo e as pontuações. Quando o jogo termina após 5 rodadas, o bot informa o vencedor e limpa as informações do jogo anterior. O jogador pode começar um novo jogo usando o comando "/start".
