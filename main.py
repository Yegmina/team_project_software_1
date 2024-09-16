import mariadb
from geopy.distance import geodesic
import tai
import random
import Yehor
import database_initializing

class Game:

    def __init__(self):
        self.money = 1000000
        self.infected_population = 1  # %
        self.public_dissatisfaction = 20  # %
        self.research_progress = 0  # %
        self.game_over = False
        self.game_turn = 0  # counter

    def start(self):
        print("Game started! Good luck!")
        self.game_turn = 1  # Reset the game turn

    def make_choice(self):
        #there should be randomly selected 3-4 choices. After player make choice from that, call payment_choice function like below
        choices = Yehor.load_choices_from_json('choices.json')
        choice_tuples = [Yehor.convert_choice_to_tuple(choice) for choice in choices]

        print(choice_tuples[0][0]) #name of the choice
        Yehor.payment_choice(self, choice_tuples[0])



    def check_game_status(self):
        if self.infected_population >= 99:
            print("The infection has spread globally. Game Over!")
            self.game_over = True
        elif self.public_dissatisfaction >= 100:
            print("Public dissatisfaction has reached critical levels. Anarchy ensues. Game Over!")
            self.game_over = True
        elif self.research_progress >= 100:
            print("The cure has been developed! You saved the world!")
            self.game_over = True

# Main game logic
def main():
    # Call the start() function from tai.py to get the user's choice
    player_choice = tai.start()

    if player_choice == 'new':
        game = Game()  # Create a new game instance
        game.start()
        # Proceed with game logic, like showing actions, making choices, etc.
        # After this line example, just for debugging purposes
        while game.game_over == False:
            game.make_choice()
            game.check_game_status()



    elif player_choice == 'continue':
        print("Loading game... (Add loading logic here)")

    elif player_choice == 'quit':
        print("Exiting the game... Goodbye! Moi moi!")


if __name__ == "__main__":
    main()

