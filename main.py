from Connection import Connection
from Character import Character
from Location import Location
from Building import Building
from Options import Options

optionsInst = Options()

'''Reads from text file, greets the player'''
def game_intro():
    intro_file = open('welcome.txt', 'r')
    print(intro_file.read())
    intro_file.close()
    optionsInst.start_options()

game_intro()

