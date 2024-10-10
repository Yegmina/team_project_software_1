import tai
import random
import Yehor
import database_manager as db
import time
import Colours
import noah as nh
import heli

class Game:

    ##---------- Initializing game's variables ----------##
    def __init__(self, name,
                 money = 10000,
                 infected_population = 3,
                 public_dissatisfaction = 7,
                 research_progress = 0,
                 game_over = False,
                 game_turn = 1,
                 infection_rate = 7,
                 max_distance = 8000,
                 new_game = 1) :

        self.name = name
        self.money = money
        self.infected_population = infected_population
        self.public_dissatisfaction = public_dissatisfaction
        self.research_progress = research_progress
        self.game_over = game_over
        self.game_turn = game_turn
        self.infection_rate = infection_rate
        self.max_distance = 8000

        self.infected_country = 1
    ##---------- Initializing game's variables ----------##

    ##---------- If it is a new game, insert it into the saved_games table. ----------##
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
                   f"{infection_rate},"
                   f"{max_distance}"
                   f")")

            # Each game' database should consist of 30 airports
            # Below is the table specifying which contients should have how many airports

            # AF - 7 ; AS - 10 ; EU - 5
            # NA - 3 ; OC - 1 ; SA - 4
            continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
            countries_each_con = (7, 10, 5, 3, 1, 4)
            length = 6

            game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}';")[0][0]
            self.id = game_id           ## If the game is new, add its id to save

            ##---------- Adding the airports to the airports database ----------##
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

            ##---------- Adding the airports to the airports database ----------##

        elif new_game == 0 :
            self.id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{self.name}';")[0][0]
            self.infected_country = db.run(f"SELECT COUNT(*) FROM airport_info "
                                           f"WHERE infected = 1 "
                                           f"AND game_id = {self.id};")[0][0]


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
        print("Make your choice!")
        time.sleep(1)
        for i in range(len(generated_choices_tuple)):
            print(f"{i + 1}. {generated_choices_tuple[i][0]}, cost {generated_choices_tuple[i][1]}")
        min_game_turn=5
        #ANOTHER TYPE OF CHOICES
        if self.game_turn>min_game_turn:
            print(f"4. Close airport by ICAO code (People will be unhappy)")
            print(f"5. Close the continent (People will be unhappy)")

        # Get user input for their cice
        print()
        print("Enter 'data' to see your current game status. Enter 'quit' to quit the game.")
        print("Enter 'airport' to see your current airports status")
        user_choice_string = input("Your choice: ")

        # Validate the input
        while not user_choice_string.isdigit() or not (1 <= int(user_choice_string) <= local_choices_amount):
            if user_choice_string == 'airport' :
                nh.print_all_icao_codes(self.id, '')
                user_choice_string = input("Your choice: ")
            elif user_choice_string == 'data' :
                heli.print_data(self.id)
                user_choice_string = input("Your choice: ")
            elif user_choice_string == 'quit' :
                self.save()
                return 'quit'
            elif not user_choice_string.isdigit():
                print("Your answer should be number")
                user_choice_string = input("Your choice: ")

            elif int(user_choice_string)==4 and self.game_turn >= min_game_turn:

                nh.print_all_icao_codes(self.id, '')
                local_icao=input("Write the ICAO code of airport that are you going to close or 'Done' to finish closing airports: ")
                if local_icao == 'Done' :
                    return

                local_boolean=nh.check_and_close_airport(self, local_icao)
                if local_boolean == True:
                    self.game_turn = self.game_turn+1

                elif local_boolean == False :
                    user_choice_string = '4'
                    continue


            elif int(user_choice_string)==5 and self.game_turn >= min_game_turn:
                nh.print_all_icao_codes(self.id, '')
                local_continent=input("Write the continent code that are you going to close or 'Done' to finishing closing continents: ")
                if local_continent == 'Done' :
                    return

                local_boolean = nh.close_continents_airports(self, local_continent)
                if local_boolean == True :
                    ## Insert increase in public dissatisfaction
                    ## Added in close_continents function
                    self.game_turn = self.game_turn + 1
                    return
                elif local_boolean == False :
                    user_choice_string = '5'
                    continue

                user_choice_string = input("Do you want to choose something else? Write your choice: ")
            else :
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
            tai.over()
            self.game_over = True
        elif self.infected_population <= 0:
            print("Everyone is healed. ")
            tai.win()
            self.game_over = True
        elif self.public_dissatisfaction >= 99:
            print("Public dissatisfaction has reached critical levels. Anarchy ensues. Game Over!")
            self.game_over = True
            tai.over()
        elif self.research_progress >= 99:
            print("The cure has been developed! You saved the world!")
            self.game_over = True
            tai.win()
        elif self.public_dissatisfaction <= 0:
            print("All people are happy about your choices! But it does not mean they are healthy!")
            self.public_dissatisfaction = 0

    def infection_spread(self):
        infected_airport_list = db.run(f"SELECT airport_id FROM airport_info "
                                       f"WHERE game_id = {self.id} "
                                       f"AND infected = 1 "
                                       f"AND closed = 0")
        if len(infected_airport_list) == 0:
            return

        for i in range(len(infected_airport_list)):
            self.airport_spread(infected_airport_list[i][0])

    def airport_spread(self, spreading_airport):

        # How far planes fly
        # Checks to see if the airport is infected and thus able to infect other countries
        if db.run(f"SELECT infected FROM airport_info "
                  f"WHERE game_id = '{self.id}' "
                  f"AND airport_id = '{spreading_airport}';")[0][0]:

            spreading_airport = Yehor.get_airport_coordinates(spreading_airport)

            # Runs through all the airports in the current game and applys the infection chance
            table = db.run(f"SELECT airport_id FROM airport_info "
                           f"WHERE game_id = '{self.id}' "
                           f"AND infected = 0 "
                           f"AND closed = 0;")
            for country1 in table:
                airport1 = Yehor.get_airport_coordinates(country1[0])

                randomNumber = random.randint(0, 100)
                if (Yehor.distance_between_two(spreading_airport, airport1) <= self.max_distance
                        and randomNumber < self.infection_rate):
                    self.infected_country += 1
                    db.run(f'UPDATE airport_info '
                           f'   SET infected = True '
                           f'WHERE airport_id = "{country1[0]}";')
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
               f"   infection_rate = {self.infection_rate}, "
               f"   max_distance = {self.max_distance} "
               f"WHERE input_name = '{self.name}';")

    # def

# Main game logic
def main():

    db.saved_games_database()
    # Call the start() function from tai.py to get the user's choice
    while True:

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
            exit()


        name, money, infected, public_diss, research, over, turn, rate, max_distance, newgame = result
        game = Game(name, money, infected, public_diss, research, over, turn, rate, max_distance, newgame)

        print("\nLoading game data...")
        print("Entering game. \n\n")

##----------------- Game starts here ------------------ ##

        while game.game_over == False:

            print('\n\n')
            s = f"Turn {game.game_turn}"

            print(f"{s:-^102}")
            print(game.public_dissatisfaction)

            time.sleep(1.5)
            heli.print_data(game.id)
            pre_choice_infected_airports = db.run(f"SELECT airport_id FROM airport_info "
                                                  f"WHERE infected = 1 "
                                                  f"AND game_id = '{game.id}'")

            ##------- Game choice -------##
            holder_value = game.make_choice()
            if holder_value == 'quit' :
                break
            game.infection_spread()
            ##------- Game choice -------##

            post_choice_infected_airports = db.run(f"SELECT airport_id FROM airport_info "
                                                   f"WHERE infected = 1 "
                                                   f"AND game_id = '{game.id}'")

            ##------ Check if there's any newly infected airport / cured airport and notify them ------##
            for infected_airport in post_choice_infected_airports :
                if infected_airport not in pre_choice_infected_airports :
                    airport_name = db.run(f"SELECT name FROM airport WHERE ident = '{infected_airport[0]}';")[0][0]
                    print((Colours.RED)+f"{airport_name} - ({infected_airport[0]}) has been infected by the disease.\n"+Colours.RESET)
                    time.sleep(0.5)
            ##------ Check if there's any newly infected airport / cured airport and notify them ------##



            ##------ Changing game variables based on random variable changes
            print()
            game.max_distance += random.randint(-10, 100)

            constant_growth = 10
            holder_value = game.infected_population
            game.infected_population = game.infected_population + int(game.infected_country / 30 * constant_growth)
            game.infected_population = min(game.infected_population, game.infected_country * 10 / 3)
            if game.infected_population - holder_value:
                print(f"The disease keeps spreading, infected population increased by {game.infected_population - holder_value} more.")

            coeff = 3 * random.random()
            holder_value = game.public_dissatisfaction
            game.public_dissatisfaction = int(game.public_dissatisfaction + (coeff ** ((game.public_dissatisfaction+game.infected_population) / 20)))
            game.public_dissatisfaction = min(game.public_dissatisfaction, 100)
            if game.public_dissatisfaction - holder_value :
                print(f"The people are not happy with your decisions. They are growing impatient. Public dissatisfaction grew {game.public_dissatisfaction - holder_value} more.")

            game.money=game.money+random.randint(0, 1000)+(100-game.infected_population)*100
            ##------ Changing game vairables

            game.check_game_status()
            game.save()



##----------------- Game ends here ------------------ ##


if __name__ == "__main__":
    db.saved_games_database()
    main()