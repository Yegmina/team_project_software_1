import mariadb
from geopy.distance import geodesic
import tai
import random
import Yehor
import database_manager as db
import time


class Game:

    db.saved_games_database()

    def __init__(self, name):
        if name == '' : pass
        name = ('game_' + db.remove_spacing(name)).lower()
        self.designated_db_table = f"{name}"           ##And initialize database
        db.create_game_database(name)
        db.run(f"INSERT INTO saved_games VALUE ('{name}');")

        self.money = 1000000
        self.infected_population = 10  # %
        self.public_dissatisfaction = 10  # %
        self.research_progress = 0  # %
        self.game_over = False
        self.game_turn = 0  # counter

    def start(self):
        print("Game started! Good luck!")
        self.game_turn = 1  # Reset the game turn

    def make_choice(self):
        choices = Yehor.load_choices_from_json('choices.json')
        choice_tuples = [Yehor.convert_choice_to_tuple(choice) for choice in choices]

        random_indices_tuple = random.sample(range(len(choice_tuples)), 3)  # This guarantees 5 unique random indices

        generated_choices_tuple = [choice_tuples[i] for i in sorted(random_indices_tuple[:3])]
        print("You should choose something!")
        time.sleep(1)
        for i in range(len(generated_choices_tuple)):

            print(f"{i+1}. {generated_choices_tuple[i][0]}, cost {generated_choices_tuple[i][1]}")
        user_choice = int(input("Your choice: "))
        Yehor.payment_choice(self, generated_choices_tuple[user_choice-1])
        #print(generated_choices_tuple)


    def check_game_status(self):
        if self.infected_population >= 99:
            print("The infection has spread globally. Game Over!")
            self.game_over = True
        elif self.infected_population <= 0:
            print("Everyone is healed. You win!")
            self.game_over = True
        elif self.public_dissatisfaction >= 100:
            print("Public dissatisfaction has reached critical levels. Anarchy ensues. Game Over!")
            self.game_over = True
        elif self.public_dissatisfaction <= 0:
            print("All people are happy about your choices! But it does not mean they are healthy!")
            self.public_dissatisfaction = 0
        elif self.research_progress >= 100:
            print("The cure has been developed! You saved the world!")
            self.game_over = True

saved_games = []              ##List of saved games



# Main game logic
def main():
    # Call the start() function from tai.py to get the user's choice
    player_choice = tai.start()

    if player_choice == 'new':

        while True:
            name = input("Enter your game name: ")
            if name == '' :
                print("The name cannot be empty\n")
                continue
            try :
                game = Game(name)
                break
            except :
                print("Please only enter characters from a..z and numbers 0..9")

        saved_games.append(game)
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