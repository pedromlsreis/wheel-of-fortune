"""

*** Wheel of Fortune ***
*** 2023 ***

Pedro Miguel Reis

"""

from __future__ import annotations
import os
import random
import re


def clean_text(s: str) -> str:
    """
    Limpa a string `s` de acentos, cedilha, leading/trailing whitespaces,
    e letras maiúsculas.

    s: string a limpar
    """
    # lidar com letras maiúsculas e espaços
    s = s.lower().strip()

    # lidar com acentos e cedilha
    s = re.sub(r'[áàãâä]', 'a', s)
    s = re.sub(r'[éèêë]', 'e', s)
    s = re.sub(r'[íìîï]', 'i', s)
    s = re.sub(r'[óòõôö]', 'o', s)
    s = re.sub(r'[úùûü]', 'u', s)
    s = re.sub(r'[ç]', 'c', s)
    s = re.sub(r'[ñ]', 'n', s)
    s = re.sub(r'[ýÿ]', 'y', s)

    return s


class Wheel:
    """
    Representa a roda da sorte.
    """
    def __init__(self: Wheel):
        """
        Inicializa a roda da sorte com as casas e respetivos valores.
        -1: Bancarrota
        -2: Ficha de recuperação
        -3: Perde Vez
        -4: Vogal Grátis
        """
        self.houses = [
            5000, -1, 750, 1000, 600, 250, -4, 1500,
            450, 200, -2, 150, 800, 900, 50, 850, 1200,
            2000, -3, 100
            ]

    def spin(self: Wheel) -> int:
        """
        Roda a roda da sorte e devolve o valor da casa onde parou.
        """
        idx = random.randint(0, len(self.houses)-1)
        return self.houses[idx]


class Puzzle:
    """
    Representa um puzzle.
    """
    def __init__(self: Puzzle, topic: str, secret: str, sep: str):
        """
        Inicializa um puzzle com o seu tema, o puzzle original, e o separador
        entre eles.

        topic: tema do puzzle
        secret: puzzle original
        sep: separador entre o tema e o puzzle
        """
        self.topic = topic
        self.sep = sep
        self.raw_secret = secret.strip()
        self.secret = clean_text(self.raw_secret)  # Puzzle limpo
        self.visible = ['-'] * len(self.secret)
        self.format_visible()
        self.existing_vowels = ""
        self.existing_consonants = ""
        self.get_existing_letters()

    def __str__(self: Puzzle) -> str:
        """
        Devolve uma string com o puzzle no formato:
        <tema>: <puzzle>
        """
        return f'{self.topic}{self.sep}{self.raw_secret}'

    def format_visible(self: Puzzle) -> list[str]:
        """
        Substitui os caracteres não alfabéticos do puzzle por eles mesmos.
        """
        for i in range(len(self.secret)):
            if not self.secret[i].isalpha():
                self.visible[i] = self.secret[i]

        return self.visible

    def find_letter(self: Puzzle, s: str) -> tuple[list[str], int]:
        """
        Atualiza a lista de caracteres visíveis com a letra presente no
        argumento `s`. Lida com letras maiúsculas, espaços, acentos e cedilha.

        s: string com a letra a procurar
        """
        # Limpa a string de acentos, cedilha, leading whitespaces e maiúsculas
        s = clean_text(s)
        count = 0

        if (not s.isalpha()) or (len(s) != 1):
            print(f'"{s}" não é uma letra válida.')
            return self.visible, count

        if s not in self.secret:
            print(f'Não há ocorrências da letra "{s}".')
            return self.visible, count

        if s in self.visible:
            print(f'A letra "{s}" já foi descoberta.')
            return self.visible, count

        if s in self.secret:
            for i in range(len(self.secret)):
                if s == self.secret[i]:
                    self.visible[i] = self.raw_secret[i]
                    count += 1

        return self.visible, count

    def get_visible(self: Puzzle) -> str:
        """
        Retorna a string de caracteres visíveis.
        """
        return f"{self.topic}{self.sep}{''.join(self.visible)}"

    def get_existing_letters(self: Puzzle):
        """
        Atualiza as listas de vogais e consoantes existentes no puzzle.
        """
        for letter in self.secret:
            if letter.isalpha():
                if letter in "aeiou":
                    self.existing_vowels += letter
                else:
                    self.existing_consonants += letter


class Puzzles:
    """
    Representa uma lista de puzzles.
    """
    def __init__(self: Puzzles, file_name: str, sep: str = ": "):
        """
        Inicializa a lista de puzzles.

        file_name: file/to/path do ficheiro de puzzles
        sep: separador entre o tema e o puzzle
        """
        self.sep = sep
        self.puzzles = self.load_puzzles(file_name)
        self.current_puzzle = None

    def load_puzzles(self: Puzzles, file_name: str) -> list[Puzzle]:
        """
        Carrega os puzzles do ficheiro `file_name` e devolve uma lista de
        puzzles.

        file_name: nome do ficheiro de puzzles
        """
        puzzles = []
        try:
            with open(file_name, 'r', encoding="utf-8") as f:
                for line in f:
                    try:
                        topic, secret = line.split(self.sep, 1)
                    except ValueError as e:
                        print(f'"{file_name}" não tem o formato correto.')
                        raise e

                    puzzles.append(Puzzle(topic, secret, self.sep))
        except FileNotFoundError as e:
            print(f'Ficheiro "{file_name}" não encontrado.')
            raise e

        return puzzles

    def set_puzzle(self: Puzzles) -> Puzzle:
        """
        Escolhe aleatoriamente um puzzle da lista de puzzles e devolve-o.
        """
        try:
            idx = random.randint(0, len(self.puzzles)-1)
        except ValueError as e:
            print('Não há puzzles para jogar.')
            self.current_puzzle = None
            raise e

        self.current_puzzle = self.puzzles[idx]
        return self.current_puzzle

    def drop_puzzle(self: Puzzles) -> list[Puzzle]:
        """
        Elimina o puzzle atual da lista de puzzles.
        """
        if not self.current_puzzle:
            print('Não há puzzle atual.')
            return self.puzzles

        self.puzzles.pop(self.puzzles.index(self.current_puzzle))
        self.current_puzzle = None
        return self.puzzles


class Player:
    def __init__(self: Player, name: str):
        """
        Inicializa um jogador com o seu nome, e o dinheiro da ronda e do jogo
        a zero, e sem fichas de recuperação.

        name: nome do jogador
        money_round: dinheiro acumulado na ronda atual
        money_game: dinheiro acumulado no jogo
        recuperacao: número de fichas de recuperação
        """
        self.name = name
        self.money_round = 0
        self.money_game = 0
        self.recuperacao = 0


class Players:
    def __init__(self: Players, names: list[str]):
        """
        Inicializa a lista de jogadores. O jogador corrente é o primeiro da
        lista.

        names: lista de nomes de jogadores
        """
        self.all = []
        self.current = 0
        for name in names:
            self.all.append(Player(name))

    def get_current_player(self: Players) -> Player:
        """
        Devolve o jogador atual da lista.
        """
        return self.all[self.current]

    def get_next_player(self: Players) -> Player:
        """
        Devolve o próximo jogador da lista.
        """
        self.current += 1
        if self.current >= len(self.all):
            self.current = 0

        return self.all[self.current]


class Game:
    def __init__(self: Game, file_name: str, names: list[str], round_no: int):
        """
        Inicializa o jogo com o número de rondas, a lista de nomes de
        jogadores, e o nome do ficheiro de puzzles.

        file_name: nome do ficheiro de puzzles
        names: lista de nomes de jogadores
        round_no: número de rondas
        """
        self.running = True  # Indica se o jogo está a correr
        self.round_no = round_no  # Número de rondas
        self.current_round = 1  # Ronda atual
        self.free_vowels = "aeiou"  # Vogais disponíveis
        self.vowel_purchase = True  # Indica se a compra de vogais está ativa
        self.free_consonants = "bcdfghjklmnpqrstvwxyz"  # Consoantes disp.
        self.wheel_active = True  # Indica se a roda da sorte está ativa
        self.commands = {
                '#': self.command_spy,
                'a': self.command_authors,
                'q': self.command_quit,
                'r': self.command_wheel,
                'i': self.command_inventario,
                'c': self.command_commands,
                'f': self.command_final,
                'p': self.command_show,
                'v': self.command_buy
            }
        # Inicializa os puzzles
        self.puzzles = Puzzles(file_name)
        if len(self.puzzles.puzzles) < self.round_no:
            self.running = False
            msg = f'Não há puzzles suficientes para jogar {self.round_no} '
            msg += 'ronda(s).'
            raise ValueError(msg)

        self.current_puzzle = self.puzzles.set_puzzle()
        # Inicializa os jogadores
        self.players = Players(names)
        self.current_player = self.players.get_current_player()
        # Inicializa a roda da sorte
        self.wheel = Wheel()

    def play_first_round(self: Game):
        """
        Joga o número de rondas indicado pelo utilizador. Se o utilizador
        terminar o jogo, o jogo termina imediatamente.
        """
        print(f" >> {self.current_puzzle.get_visible()}")
        print(f"Início da ronda número {self.current_round}")

    def spin(self: Game) -> int:
        """
        Faz girar a roleta e devolve o valor da casa onde parou.
        """
        return self.wheel.spin()

    def bancarrota(self: Game):
        """
        O jogador perde todo o dinheiro obtido nesta ronda e também perde a
        vez.
        """
        msg = '"Bancarrota". Perde todo o dinheiro obtido nesta ronda e também'
        msg += ' perde a vez.'
        print(msg)
        self.current_player.money_round = 0
        self.ficha_recuperacao()

    def ganha_ficha_recuperacao(self: Game):
        """
        Permite ao jogador receber uma ficha de recuperação.
        """
        print('"Ficha de recuperação". Boa! Ganhou uma ficha de recuperação.')
        self.current_player.recuperacao += 1

    def perde_vez(self: Game):
        """
        O jogador perde a sua vez, passando para o próximo jogador.
        """
        print('"Perde vez". Perdeu a sua vez de jogar.')
        self.ficha_recuperacao()

    def vogal_gratis(self: Game):
        msg = '"Vogal grátis". Qual a vogal? '
        vowel = str(input(msg))
        vowel = clean_text(vowel)

        # A letra indicada não é uma vogal
        if vowel not in "aeiou":
            print(f'"{vowel}" não é uma letra válida.')
            print("Perde a vez. Para a próxima esteja com mais atenção.")
            self.ficha_recuperacao()

        # A vogal é válida mas já foi levantada
        elif vowel not in self.free_vowels:
            print(f'"{vowel}" já foi levantada.')
            print("Perde a vez. Para a próxima esteja com mais atenção.")
            self.ficha_recuperacao()

        # A vogal é válida
        else:
            self.free_vowels = self.free_vowels.replace(vowel, "")
            if len(self.free_vowels) == 0:
                self.vowel_purchase = False

            if vowel in self.current_puzzle.secret:
                _, count = self.current_puzzle.find_letter(vowel)
                if count > 0:
                    msg = f'Encontrada(s) {count} ocorrência(s) de "{vowel}".'
                    print(msg)
                    print(f" >> {self.current_puzzle.get_visible()}")
                else:
                    print(f'Não foram encontradas ocorrências de "{vowel}".')
                    print(f" >> {self.current_puzzle.get_visible()}")

    def ficha_recuperacao(self: Game):
        """
        Pergunta ao jogador se quer usar uma ficha de recuperação,
        caso tenha alguma.
        """
        if self.current_player.recuperacao > 0:
            msg = "Você vai perder a vez. Deseja usar agora uma ficha"
            msg += " de recuperação (s/n)? "
            r = str(input(msg))
            r = clean_text(r)
            if r == "s":
                print("Afinal não perde a vez.")
                self.current_player.recuperacao -= 1
            else:
                self.current_player = self.players.get_next_player()
        else:
            self.current_player = self.players.get_next_player()

    def wheel_houses(self: Game, result: str):
        """
        Interpreta o resultado negativo da roleta e executa a ação
        correspondente.
        """
        if result == -1:
            # Bancarrota
            self.bancarrota()
        elif result == -2:
            # Ficha de recuperação
            self.ganha_ficha_recuperacao()
        elif result == -3:
            # Perde Vez
            self.perde_vez()
        elif result == -4:
            # Vogal Grátis
            self.vogal_gratis()

    def next_round(self: Game):
        """
        Inicia a próxima ronda.
        """
        if self.current_round == self.round_no:
            self.end_game()
        else:
            self.current_round += 1
            print(f"Início da ronda número {self.current_round}")
            self.puzzles.drop_puzzle()
            self.current_puzzle = self.puzzles.set_puzzle()
            self.free_vowels = "aeiou"
            self.vowel_purchase = True
            self.free_consonants = "bcdfghjklmnpqrstvwxyz"
            self.wheel_active = True
            msg = f"Resolva o puzzle! >> {self.current_puzzle.get_visible()}"
            print(msg)

    def end_game(self: Game):
        """
        Termina o jogo.
        """
        print(f"Final do jogo! Este jogo teve {self.round_no} ronda(s).")
        BONUS = 6000

        # Encontra o(s) vencedore(s)
        tied_winners = []
        winner = self.players.all[0]
        for player in self.players.all:
            if player.money_game >= winner.money_game:
                if player.money_game > winner.money_game:
                    winner = player
                    tied_winners = []
                elif player.money_game == winner.money_game:
                    tied_winners.append(player)

        # Distribui o prémio pelos vencedores
        if len(tied_winners) > 0:
            for player in tied_winners:
                player.money_game += BONUS // len(tied_winners)
        else:
            winner.money_game += BONUS

        # Apresenta os resultados
        if len(tied_winners) == 0:
            for player in self.players.all:
                if player == winner:
                    msg = f'O concorrente "{player.name}" venceu o jogo e'
                    msg += f' leva para casa {player.money_game} euros.'
                    print(msg)
                else:
                    msg = f'O concorrente "{player.name}" leva para casa'
                    msg += f' {player.money_game} euros.'
                    print(msg)
        else:
            for player in self.players.all:
                if player in tied_winners:
                    msg = f'O concorrente "{player.name}" venceu o jogo e'
                    msg += f' leva para casa {player.money_game} euros.'
                    print(msg)
                else:
                    msg = f'O concorrente "{player.name}" leva para casa'
                    msg += f' {player.money_game} euros.'
                    print(msg)

        self.running = False

    def spy(self: Game):
        """
        Apresenta informação técnica.
        Não é considerado um método de interação com o utilizador.
        """
        print("  Spy:")
        wa = self.wheel_active * 1
        vp = self.vowel_purchase * 1
        cpz = self.current_puzzle
        print(f"# {self.current_round} {wa} {vp}")
        print(f"# {cpz.topic}: {cpz.raw_secret}")
        print(f"# {cpz.get_visible()}")
        for p in self.players.all:
            is_curr = "*" if p == self.current_player else "-"
            # convert money round in 5 digits
            mr = str(p.money_round)
            mr = "0" * (5 - len(mr)) + mr
            # convert money game in 5 digits
            mg = str(p.money_game)
            mg = "0" * (5 - len(mg)) + mg
            print(f"# {is_curr} {p.recuperacao} {mr} {mg} {p.name}")


def mooshak():
    """
    Função necessária para o Mooshak.
    Não altere esta função!
    """
    FILE_NAME = "puzzles.txt"
    m = os.environ.get('MOOSHAK')
    if m:
        eval(m)
        return os.environ.get('MOOSHAK_PUZZLES')
    else:
        return FILE_NAME


class UI:
    """
    Representa a interface do utilizador.
    """
    def __init__(self: UI):
        """
        Inicializa a interface do utilizador.
        """
        self.round_no, self.player_no, self.names = self.set_initial_info()
        file_name = mooshak()
        self.game = Game(file_name, self.names, self.round_no)

    def welcome(self: UI):
        """
        Apresenta uma mensagem de boas-vindas e inicia o jogo.
        """
        print("Vamos começar. Eis o puzzle. Boa sorte!")
        # Inicializa o jogo
        self.game.play_first_round()

    def set_initial_info(self: UI) -> tuple[int, int, list[str]]:
        """
        Pede ao utilizador o número de rondas, o número de concorrentes e os
        seus nomes.
        """
        print('Bem-vindo/a ao jogo "A Roda da Sorte"!')
        round_no = int(input("Quantas rondas? "))
        if not (1 <= round_no <= 4):
            print("O número de rondas não é válido, deverá ser entre 1 e 4.")
            return self.set_initial_info()

        player_no = int(input("Quantos concorrentes? "))
        if not (1 <= player_no <= 4):
            msg = "O número de concorrentes não é válido, deverá ser entre 1"
            msg += " e 4."
            print(msg)
            return self.set_initial_info()

        player_names = []
        for i in range(1, player_no+1):
            name = str(input(f"Nome do concorrente número {i}? "))
            if (name in player_names) or (not name) or (not name.isalpha()):
                print("Nome inválido, tente novamente.")
                return self.set_initial_info()

            player_names.append(name)

        return round_no, player_no, player_names

    def input_command(self: UI) -> str:
        """
        Lê um comando do utilizador.
        """
        cp = self.game.current_player
        command_line = input(f"[{cp.name}]: ")
        command = clean_text(command_line)
        return command

    def command_spy(self: UI):
        """
        Apresenta informação técnica.
        """
        self.game.spy()

    def command_authors(self: UI):
        """
        Apresenta os autores do programa.
        """
        print("  Autores:")
        print("\tPedro Miguel Reis")

    def command_quit(self: UI):
        """
        Termina o jogo imediatamente.
        """
        print("  Adeus!")
        self.game.running = False

    def command_help(self: UI):
        """
        Apresenta uma mensagem de ajuda.
        """
        print("  Comando inválido! Ajuda:")
        msg = "\tPressione `c` seguido de `Enter` para listar os comandos"
        msg += " possíveis."
        print(msg)
        print("\tÉ possível usar letras maiúsculas ou minúsculas.")

    def command_commands(self: UI):
        """
        Apresenta uma lista de comandos.
        """
        print("  Comandos:")
        print("\tc - Comandos (listar comandos)")
        print("\ti - Inventário (mostrar)")
        print("\tf - Finalizar puzzle")
        print("\tp - Puzzle (mostrar)")
        print("\tr - Roleta (rodar)")
        print("\tv - Vogal (comprar)")
        print("\t# - Espiar (mooshak)")
        print("\tq - Quit (terminar imediatamente)")

    def command_inventario(self: UI):
        """
        Apresenta o inventário dos jogadores.
        """
        print("  Inventário:")
        print("\tN.  Nome                Fichas   Ronda    Jogo")
        for idx, player in enumerate(self.game.players.all):
            p_id = idx + 1
            p_name = player.name
            p_recuperacao = player.recuperacao
            p_money_round = player.money_round
            p_money_game = player.money_game
            msg = f"\t{p_id}{' '*max(0, 4-len(str(p_id)))}"
            msg += f"{p_name}{' '*max(0, 20-len(p_name))}"
            msg += f"{p_recuperacao}{' '*max(0, 9-len(str(p_recuperacao)))}"
            msg += f"{p_money_round}{' '*max(0, 9-len(str(p_money_round)))}"
            msg += f"{p_money_game}"
            print(msg)

    def command_final(self: UI):
        """
        Permite ao utilizador resolver o puzzle.
        """
        cpz = self.game.current_puzzle
        msg = f"Resolva o puzzle! >> {cpz.topic}{cpz.sep}"
        f = clean_text(str(input(msg)))
        if f == clean_text(cpz.secret):
            cp = self.game.current_player
            print("Certo!")
            msg = f'O concorrente "{cp.name}" venceu a ronda número'
            msg += f' {self.round_no}.'
            print(msg)
            cp.money_game += cp.money_round
            cpz.visible = cpz.raw_secret
            self.game.wheel_active = False
            self.game.vowel_purchase = False
            cp.money_round = 0
            for player in self.game.players.all:
                if player != cp:
                    player.money_round = 0
            self.command_inventario()
            self.game.next_round()
        else:
            print("Errado. Perde a vez.")
            self.game.ficha_recuperacao()

    def command_show(self: UI):
        """
        Apresenta o puzzle atual.
        """
        print(" >>", self.game.current_puzzle.get_visible())

    def command_buy(self: UI):
        """
        Permite ao utilizador comprar uma vogal.
        """
        cp = self.game.current_player
        fv = self.game.free_vowels
        if cp.money_round >= 250:
            vowel = str(input("Qual a vogal? "))
            vowel = clean_text(vowel)
            cp.money_round -= 250
            if vowel not in fv:
                print(f'"{vowel}" já foi levantada.')
                print("Perde a vez. Para a próxima esteja com mais atenção.")
                self.game.ficha_recuperacao()
            else:
                self.game.free_vowels = fv.replace(vowel, "")
                if len(self.game.free_vowels) == 0:
                    self.game.vowel_purchase = False
                if vowel in self.game.current_puzzle.secret:
                    _, count = self.game.current_puzzle.find_letter(vowel)
                    if count > 0:
                        msg = f'Encontrada(s) {count} ocorrência(s) de '
                        msg += f'"{vowel}".'
                        print(msg)
                        print(f" >> {self.game.current_puzzle.get_visible()}")
                    else:
                        msg = 'Não foram encontradas ocorrências de '
                        msg += f'"{vowel}".'
                        print(msg)
                        print(f" >> {self.game.current_puzzle.get_visible()}")
                else:
                    print(f'Não foram encontradas ocorrências de "{vowel}".')
                    print(f" >> {self.game.current_puzzle.get_visible()}")
                    self.game.ficha_recuperacao()
        else:
            print("Você não tem dinheiro suficiente para comprar uma vogal.")
            print("Perde a vez. Para a próxima esteja com mais atenção.")
            self.game.ficha_recuperacao()

    def command_wheel(self: UI):
        curr_puzzle = self.game.current_puzzle
        result = self.game.spin()

        # Se o resultado for negativo, executa a ação correspondente
        if result < 0:
            self.game.wheel_houses(result)
        else:
            cons = str(input(f"{result}. Qual a consoante? "))
            cons = clean_text(cons)

            fc = self.game.free_consonants

            if (len(cons) != 1) or \
                    (cons not in "bcdfghjklmnpqrstvwxyz"):
                print(f'"{cons}" não é uma letra válida.')
                print("Perde a vez. Para a próxima esteja com mais atenção.")
                self.game.current_player = self.game.players.get_next_player()

            elif (cons in curr_puzzle.visible) or \
                    (cons not in fc):
                print(f'A letra "{cons}" já saiu e está à vista.')
                print("Perde a vez. Para a próxima esteja com mais atenção.")
                self.game.current_player = self.game.players.get_next_player()

            elif cons in curr_puzzle.secret:
                _, count = curr_puzzle.find_letter(cons)
                fc = fc.replace(cons, "")
                cpz = self.game.current_puzzle
                cpz.existing_consonants = cpz.existing_consonants.replace(
                    cons, "")
                if len(cpz.existing_consonants) == 0:
                    self.game.wheel_active = False
                if count > 0:
                    mult = count * result
                    self.game.current_player.money_round += mult
                    # Cria a mensagem a apresentar
                    msg = f'Encontrada(s) {count} ocorrência(s) de "{cons}"'
                    msg += f' valendo {count}*{result}={mult}. '
                    # Atualiza a mensagem com o dinheiro de cada jogador
                    name_and_money = []
                    for player in self.game.players.all:
                        name_and_money.append(
                            f'{player.name} = {player.money_round}'
                            )
                    msg += f'{", ".join(name_and_money)}.'

                    print(msg)
                    print(f" >> {curr_puzzle.get_visible()}")
                else:
                    print(f'Não foram encontradas ocorrências de "{cons}".')
                    self.game.ficha_recuperacao()
            else:
                print(f'Não foram encontradas ocorrências de "{cons}".')
                self.game.ficha_recuperacao()

    def interpreter(self: UI):
        """
        Interpreta os comandos do utilizador.
        """
        while self.game.running:
            command = self.input_command()
            if command in self.commands:
                self.commands[command]()
            else:
                self.command_help()

        self.command_spy()

    def run(self: UI):
        """
        Inicia o jogo.
        """
        self.welcome()
        self.interpreter()
        print("Adeus!")


def main():
    ui = UI()
    ui.run()


main()
