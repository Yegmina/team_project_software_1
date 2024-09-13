import random
import mysql.connector


connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database = 'flight_game',
    password = '1234',
    collation = 'utf8mb4_general_ci',
    autocommit = True
)
cursor = connection.cursor()

class Game :

    def __init__(self):                     ## Declaring Global Variables

        self.game_running = True
        pass

    def StartGame(self):                    ## Game Start
        while self.game_running:

            self.make_choice()
            self.check_game_status()

        pass

    def check_game_status(self):            ## Check if game should be running

        pass

    def make_choice(self):
        print("[Insert Choice]")
        # choice = input()
        pass

    def print_status(self):

        pass

newGame = Game()
print("[Prototype start button]")
print("Press ENTER to start")
StartSignal = input()

if StartSignal == '' :
    newGame.StartGame()


