import database_manager as db


def new_game() :
    while True:

        name = input("Enter your game name: ")
        name_list = db.run(f"SELECT * FROM saved_games WHERE input_name = '{name}';")
        ##Checking if there is a game with that name
        if len(name_list) == 0:
            pass
        elif name == '':
            print("The name cannot be empty\n")  ##Self-explanatory
            continue
        elif len(name_list) != 0:
            print_data(name_list[0][0])
            print("Profile already exists.\nDo you want to play on this profile instead?")
            while True :
                try :
                    player_choice = int(input("Yes, I want to play on this profile (enter `1`) "
                                              "or No, I want to create a new profile(enter `2`): "))
                    break
                except :
                    print("Please enter 1 or 2.")
                    pass
                finally :
                    if player_choice < 1 or player_choice > 2 :
                        print("Please enter 1 or 2.")
                        continue
            if player_choice == 1 :
                gsf = name_list[0]          ## Game stats fetch
                game_stats = (gsf[1], gsf[2], gsf[3], gsf[4], gsf[5], gsf[6], gsf[7], gsf[8], gsf[9], 0)
                ## 0 at the end is for new_game = 0
                return game_stats

            elif player_choice == 2 :
                continue
                                                                ##Checking if there's already been a
            continue                                            ##game with the inputted name
                                                                ## IDEA : We could add an option for the player to choose
        return name, 10000, 3, 7, 0, False, 1, 7, 8000, 1       ## play the profile with the existing name if the name were
                                                                ## to be a duplicate

        ##This returns a tuple to declare a new game.


def continue_game() :
    all_saved_games = db.run("SELECT * FROM saved_games")

    if len(all_saved_games) == 0 :
        print("It looks like currently you don't have any games stored.\n"
              "Do you want to create a new game?")
        while True:
            try :
                option = int(input("YES (1) or NO (2): "))
                if option != 1 and option != 2 :
                    continue
                break
            except :
                print("Please enter 1 or 2.")
        return option

    else :
        return 0


def fetch_game() :
    all_saved_games = db.run("SELECT * FROM saved_games")
    input_name = 1 #Input_name column is the second column in saved_games table

    while True :
        print()
        for i in range(len(all_saved_games)):
            print(f"{i + 1}. {all_saved_games[i][input_name]}")  ##Input
        try :
            game_option = int(input("Select your game (Enter 0 to create a new game): "))
            if game_option < 0 or game_option > len(all_saved_games) :
                print(f"Please enter a number from 1 to {len(all_saved_games)}.")
                continue
            #  print the data of game (result)
            #  print(all_saved_games[game_option - 1])
            if game_option == 0 :
                return new_game()

            print_data(all_saved_games[game_option - 1][0])
            #print data from all_saved_games[game_option - 1]
            print("Are you sure about this game ?")

            correct_input, sure = False, True
            while correct_input == 0:

                try :
                    c = int(input('YES (1) or NO (2): '))
                    if c == 1 :
                        gsf = all_saved_games[game_option - 1]
                        return gsf[1], gsf[2], gsf[3], gsf[4], gsf[5], gsf[6], gsf[7], gsf[8], gsf[9], 0

                    elif c == 2:
                        correct_input = True
                        sure = False
                        continue
                    else :
                        print('Please enter 1 or 2.')
                except :
                    print("Please enter 1 or 2.")
                    pass

            if sure == 0 :
                continue

        except :
            print(f"Please enter a number from 1 to {len(all_saved_games)}.")

    game_option -= 1


def print_data(game_id) :
    game_data = db.run(f"SELECT * FROM saved_games WHERE id = '{game_id}';")
    (money, infected_population, public_dissastisfaction, research_progress, game_turns, infection_rate) = 2, 3, 4, 5, 7, 8
    print(f"+{'':-^16}+{'':-^21}+{'':-^22}+{'':-^17}+{'':-^20}+")

    print(f"|{'MONEY': ^16}|{'INFECTED POPULATION': ^21}|{'PUBLIC DISSATISFACTION': ^22}|"
          f"{'RESEARCH PROGRESS': ^16}|{'INFECTION RATE': ^20}|")

    print(f"|{'':-^16}+{'':-^21}+{'':-^22}+{'':-^17}+{'':-^20}|")

    print(f"|{game_data[0][money]:^16}"
          f"|{game_data[0][infected_population] :^21}"
          f"|{game_data[0][public_dissastisfaction] :^22}"
          f"|{game_data[0][research_progress] :^17}"
          f"|{game_data[0][infection_rate] : ^ 20}|")

    print(f"+{'':-^16}+{'':-^21}+{'':-^22}+{'':-^17}+{'':-^20}+")
