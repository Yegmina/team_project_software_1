import mariadb
from geopy.distance import geodesic
import tai
import random
import Yehor
import database_manager as db
import time


class Game:

    def __init__(self, name,
                 money = 1000000,
                 infected_population = 10,
                 public_dissatisfaction = 10,
                 research_progress = 0,
                 game_over = False,
                 game_turn = 0) :

        self.name = name
        self.money = money
        self.infected_population = infected_population
        self.public_dissatisfaction = public_dissatisfaction
        self.research_progress = research_progress
        self.game_over = game_over
        self.game_turn = game_turn

        db.run(f"INSERT INTO saved_games VALUES"
               f"(id,"
               f"'{name}', "
               f"{money}, "
               f"{infected_population},"
               f"{public_dissatisfaction},"
               f"{research_progress},"
               f"{game_over},"
               f"{game_turn}"
               f")")

        # AF - 7 ; AS - 10 ; EU - 5
        # NA - 3 ; OC - 1 ; SA - 4
        continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
        countries_each_con = (7, 10, 5, 3, 1, 4)
        length = 6
        game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}'")[0][0]
        for index in range(length):
            game_airports = []

            airports = db.run(f"SELECT ident FROM airport "
                              f"WHERE type = 'large_airport' "
                              f"AND continent = '{continents[index]}';")

            for num in range(countries_each_con[index]):

                rand = random.randint(0, len(airports) - 1)
                while airports[rand][0] in game_airports:
                    rand = random.randint(0, len(airports) - 1)

                game_airports.append(airports[rand][0])

            for airport in game_airports:
                db.run(f"INSERT INTO airport_info VALUES ('{game_id}', '{airport}', 0, 0)")



    def start(self):
        print("Game started! Good luck!")
        self.game_turn = 1  # Reset the game turn

    def make_choice(self):
        choices = Yehor.load_choices_from_db()
        choice_tuples = [Yehor.convert_choice_to_tuple(choice) for choice in choices]
        local_choices_amount=3
        random_indices_tuple = random.sample(range(len(choice_tuples)), local_choices_amount)  # This guarantees 3 unique random indices

        generated_choices_tuple = [choice_tuples[i] for i in sorted(random_indices_tuple[:local_choices_amount])]
        print("You should choose something!")
        time.sleep(1)
        for i in range(len(generated_choices_tuple)):

            print(f"{i+1}. {generated_choices_tuple[i][0]}, cost {generated_choices_tuple[i][1]}")

        user_choice_string = input("Your choice: ")

        while not user_choice_string.isdigit() or not (1 <= int(user_choice_string) <= 3):
            print("Invalid choice!")
            user_choice_string = input("Your choice: ")
        user_choice = int(user_choice_string)

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

    def save(self):
        # Corrected SQL syntax
        db.run(f"UPDATE saved_games "
               f"SET money = {self.money}, "
               f"   infected_population = {self.infected_population}, "
               f"   public_dissatisfaction = {self.public_dissatisfaction}, "
               f"   research_progress = {self.research_progress}, "
               f"   game_over = {self.game_over}, "
               f"   game_turn = {self.game_turn} "
               f"WHERE input_name = '{self.name}';")

    ##Outputting game data function here
    def print_data(self):                   ##Will have to rewrite __init__ to specify
        pass                                ##Game() initializing to have variables


# Main game logic
def main():

    db.saved_games_database()

    # Call the start() function from tai.py to get the user's choice
    player_choice = tai.start()

    if player_choice == 'new':

        while True:
            name = input("Enter your game name: ")
            name_list = db.run(f"SELECT input_name FROM saved_games WHERE input_name = '{name}';")
            ##Checking if there is a game with that name
            if name == '' :
                print("The name cannot be empty\n")     ##Self-explanatory
                continue
            elif len(name_list) != 0 :
                print("Profile already exists")         ##Checking if there's already been a
                                                        ##game with the inputted name
            game = Game(name)
            break

        # Proceed with game logic, like showing actions, making choices, etc.
        # After this line example, just for debugging purposes
        while game.game_over == False:
            game.make_choice()
            game.check_game_status()
            game.save()



    elif player_choice == 'continue':
        print("Loading game... (Add loading logic here)")


    elif player_choice == 'quit':
        print("Exiting the game... Goodbye! Moi moi!")


if __name__ == "__main__":
    db.saved_games_database()
    main()