"""

*** Wheel of Fortune ***
*** 20XX ***
 
Pedro Miguel Reis

"""

############# import #############

from __future__ import annotations
import random
import os


############# Wheel #############

class Wheel:
    def __init(self: Wheel):
        pass
    
    def random_index(self: Wheel) -> int:
        # pode usar random.randint da prática 13
        pass
 

############# Puzzle #############

class Puzzle:
    def __init__(self: Puzzle, secret: str):
        self.secret = secret
        self.visible = ['-'] * len(secret)   # é preciso usar uma lista mutável
    
    def get_visible() -> str:
        ''.join(self.visible)


############# Puzzles #############

class Puzzles:
    def __init(self: Puzzles, file_name: str):
        self.puzzles = []           # todos os puzzles
        self.load(file_name)

    def load(self: Puzzles, file_name: str):
        # carrega todos os puzzles
        # inspire-se no 3º exemplo da teórica 17
        pass     


############# Player #############

class Player:
    def __init__(self: Player, name: str):
        self.name = name


############# Players #############

class Players:
    def __init__(self: Players, names: list[str]):
        self.all = []
        self.current = 0
        for name in names:
            self.all.append(Player(name))
    
    def get_current_player(self: Players) -> Player:
        return self.all[self.current]


############# Game #############

class Game:
    def __init__(self: Game, file_name: str, names: list[str]):
        self.players = Players(names)
        self.running = True
        
    def get_current_player(self: Game) -> Player:
        return self.players.get_current_player()
    
    # O método spy escreve informação técnica.
    # Não é considerado um método de interação com o utilizador.
    # É mais prático definir o método aqui do que na classe UI.
    def spy(self: Game):
        print("# SPY")


############# Mooshak #############

# Não altere esta função!

def mooshak():
    FILE_NAME = "puzzles.txt"
    m = os.environ.get('MOOSHAK')
    if m:
        eval(m)
        return os.environ.get('MOOSHAK_PUZZLES')
    else:
        return FILE_NAME


############# UI #############

class UI:   # User Interface
    def __init__(self: UI):
        file_name = mooshak()              # linha necessária
        self.game = Game(file_name, ["jeremias"])
   
    def error(self: UI, mesg: str):
        raise Exception(f"{mesg}!")
    
    def welcome(self: UI):
        print("Blá Blá Blá")
    
    def input_command(self: UI) -> str:
        p = self.game.get_current_player()
        command_line = input(f"[{p.name}]: ")
        command = command_line.strip().upper()
        return command
    
    def command_spy(self: UI):
        self.game.spy()        # linha necessária
    
    def command_authors(self: UI):
        print("Autores:")
        print("   Nº12345 Maria Imaginária")
        print("   Nº54321 Mário Virtual")
    
    def command_quit(self: UI):
        pass
    
    def command_help(self: UI):
        pass
    
    def interpreter(self: UI):
        # inspire-se no interpretador do final da teórica 18
        while self.game.running:
            command = self.input_command()
            if command == ' ': pass
            if command == '#': self.command_spy()
            if command == 'A': self.command_authors()
            elif command == 'Q': return self.command_quit()
            else: self.command_help()
        self.command_spy()        # linha necessária
    
    def run(self: UI):
        self.welcome()
        self.interpreter()


############# main #############

def main():
    ui = UI()
    ui.run()

main()
