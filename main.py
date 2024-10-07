import mariadb
from geopy.distance import geodesic
import tai
import random
import Yehor
import database_manager as db
import time

import heli


class Game:

    def __init__(self, name,
                 money = 1000000,
                 infected_population = 10,
                 public_dissatisfaction = 10,
                 research_progress = 0,
                 game_over = False,
                 game_turn = 0,
                 infection_rate = 5,
                 new_game = 1) :

        self.name = name
        self.money = money
        self.infected_population = infected_population
        self.public_dissatisfaction = public_dissatisfaction
        self.research_progress = research_progress
        self.game_over = game_over
        self.game_turn = game_turn
        self.infection_rate = infection_rate

        if new_game == 1:
            db.run(f"INSERT INTO saved_games VALUES"
                   f"(id,"
                   f"'{name}', "
                   f"{money}, "
                   f"{infected_population},"
                   f"{public_dissatisfaction},"
                   f"{research_progress},"
                   f"{game_over},"
                   f"{game_turn},"
                   f"{infection_rate}"
                   f")")

            # AF - 7 ; AS - 10 ; EU - 5
            # NA - 3 ; OC - 1 ; SA - 4
            continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
            countries_each_con = (7, 10, 5, 3, 1, 4)
            length = 6
            game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}';")[0][0]
            self.id = game_id
            game_airports = []
            game_airports_countries = []
            for index in range(length):

                airports = db.run(f"SELECT ident, iso_country FROM airport "
                                  f"WHERE type = 'large_airport' "
                                  f"AND continent = '{continents[index]}';")
                for num in range(countries_each_con[index]):

                    rand = random.randint(0, len(airports) - 1)
                    while airports[rand][0] in game_airports or airports[rand][1] in game_airports_countries:
                        rand = random.randint(0, len(airports) - 1)

                    game_airports.append(airports[rand][0])
                    game_airports_countries.append(airports[rand][1])

            for airport in game_airports:
                db.run(f"INSERT INTO airport_info VALUES ('{game_id}', '{airport}', 0, 0)")

            first_infected_airport = random.randint(0, 29)
            db.run(f"UPDATE airport_info "
                   f"SET "
                   f"   infected = 1 "
                   f"WHERE airport_id = '{game_airports[first_infected_airport]}';")

        elif new_game == 0 :
            self.id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}';")[0][0]




    def start(self):
        print("Game started! Good luck!")
        self.game_turn = 1  # Reset the game turn

    def make_choice(self):
        # Load all choices from the database
        choices = Yehor.load_choices_from_db()
        choice_tuples = [Yehor.convert_choice_to_tuple(choice) for choice in choices]

        # Get choices already made by the user for this game
        game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}';")[0][0]
        already_made_choices = db.run(f"SELECT choice_id FROM choices_made WHERE game_id = {game_id};")
        already_made_choice_ids = {row[0] for row in already_made_choices}

        # Filter out choices that have already been made
        available_choices = [choice for choice in choice_tuples if
                             db.run(f"SELECT id FROM choices WHERE name = '{choice[0]}'")[0][
                                 0] not in already_made_choice_ids]

        # Handle the case where there are no available choices left
        if not available_choices:
            print("You have already made all available choices.")
            return

        # Randomly select 3 available choices (or less if fewer than 3 are left)
        local_choices_amount = min(3, len(available_choices))
        random_indices_tuple = random.sample(range(len(available_choices)),
                                             local_choices_amount)  # unique random indices
        generated_choices_tuple = [available_choices[i] for i in sorted(random_indices_tuple[:local_choices_amount])]

        # Prompt the user to choose
        print("You should choose something!")
        time.sleep(1)
        for i in range(len(generated_choices_tuple)):
            print(f"{i + 1}. {generated_choices_tuple[i][0]}, cost {generated_choices_tuple[i][1]}")

        # Get user input for their choice
        user_choice_string = input("Your choice: ")

        # Validate the input
        while not user_choice_string.isdigit() or not (1 <= int(user_choice_string) <= local_choices_amount):
            print("Invalid choice!")
            user_choice_string = input("Your choice: ")

        user_choice = int(user_choice_string)
        chosen_tuple = generated_choices_tuple[user_choice - 1]

        # Process the choice
        choice_name = chosen_tuple[0]
        choice_id = db.run(f"SELECT id FROM choices WHERE name = '{choice_name}'")[0][0]

        # Save the choice as made
        Yehor.payment_choice(self, chosen_tuple)

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

    def infection_spread(self):
        infected_airport_list = db.run(f"SELECT airport_id FROM saved_games "
                                       f"LEFT JOIN airport_info on airport_info.game_id = saved_games.id "
                                       f"WHERE input_name = '{self.name}' "
                                       f"AND infected = 1 "
                                       f"AND closed = 0;")
        if len(infected_airport_list) == 0:
            return

        for i in range(len(infected_airport_list)):
            self.airport_spread(infected_airport_list[i][0])

    def airport_spread(self, spreading_airport):

        # How far planes fly
        plane_flight_distance = 2000

        # Checks to see if the airport is infected and thus able to infect other countries
        if db.run(f"SELECT infected FROM airport_info "
                  f"WHERE game_id = '{self.id}' "
                  f"AND airport_id = '{spreading_airport}';")[0][0]:
            spreading_airport = Yehor.get_airport_coordinates(spreading_airport)

            # Runs through all the airports in the current game and applys the infection chance
            table = db.run(f"SELECT airport_id FROM airport_info WHERE game_id = '{self.id}';")
            for country1 in table:
                airport1 = Yehor.get_airport_coordinates(country1[1])

                if (Yehor.distance_between_two(spreading_airport, airport1) < plane_flight_distance
                        and random.randint(0,100) < self.infection_rate):
                    db.run(f'UPDATE airport_info '
                           f'SET infected = True '
                           f'WHERE airport_id = {country1[1]};')
        else:
            return

    def save(self):
        # Corrected SQL syntax
        db.run(f"UPDATE saved_games "
               f"SET money = {self.money}, "
               f"   infected_population = {self.infected_population}, "
               f"   public_dissatisfaction = {self.public_dissatisfaction}, "
               f"   research_progress = {self.research_progress}, "
               f"   game_over = {self.game_over}, "
               f"   game_turn = {self.game_turn}, "
               f"   infection_rate = {self.infection_rate} "
               f"WHERE input_name = '{self.name}';")

    # def


# Main game logic
def main():

    db.saved_games_database()
    # Call the start() function from tai.py to get the user's choice
    while True :
        player_choice = tai.start()

        ##result = Game()

        if player_choice == 'new':
            result = heli.new_game() ## Will transfer to tai.py

        # Proceed with game logic, like showing actions, making choices, etc.
        # After this line example, just for debugging purposes

        elif player_choice == 'continue':
            branch_output = heli.continue_game()

            if branch_output == 0 : ## Find game inside the game list
                result = heli.fetch_game()
                pass

            elif branch_output == 1 : ## The game list is empty
                result = heli.new_game() ## Will transfer to tai.py
                pass

            elif branch_output == 2 : ## No want new game
                continue
                pass


        elif player_choice == 'quit':
            print("Exiting the game... Goodbye! Moi moi!")
            pass


        name, money, infected, public_diss, research, over, turn, rate, newgame = result
        game = Game(name, money, infected, public_diss,
                    research, over, turn, rate, newgame)


        print("\nLoading game data...")
        print("Entering game. \n\n")

##----------------- Game starts here ------------------ ##

        while game.game_over == False :

            pre_choice_infected_airports = db.run(f"SELECT airport_id FROM airport_info "
                                                  f"WHERE infected = 1")

    ##------- Game choice -------##
            game.make_choice()
            game.infection_spread()
    ##------- Game choice -------##

            post_choice_infected_airports = db.run(f"SELECT airport_id FROM airport_info "
                                                   f"WHERE infected = 1")

            ##------ Check if there's any newly infected airport / cured airport and notify them ------##
            for infected_airport in post_choice_infected_airports :
                if infected_airport not in pre_choice_infected_airports :
                    print(f"{infected_airport} has been infected by the disease.")
            ##------ Check if there's any newly infected airport / cured airport and notify them ------##


            game.check_game_status()

            game.save()

##----------------- Game ends here ------------------ ##


if __name__ == "__main__":
    db.saved_games_database()
    main()