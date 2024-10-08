import database_manager as db

def start():
    print("WELCOME TO AIRPORT GAME!! (Press Enter to continue)")
    input()  # Pause for user to press Enter

    input("This game is about managing airport logistics...")  # Game description

    print("Rules          : R(1)\n"
          "New Game       : N(2)\n"
          "Continue       : C(3)\n"
          "Quit           : Q(4)\n")


    while True:
        try:
            Start_choice = int(input("Enter your choice: "))
            if Start_choice == 1:
                print("RULES: Manage the airport, control the virus spread, and develop a cure.")
            elif Start_choice == 2:
                print("Starting a New Game...")
                return 'new'
            elif Start_choice == 3:
                print("Loading previous game...")
                return 'continue'
            elif Start_choice == 4:
                print("Goodbye!")
                return 'quit'
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
#design game over
def over():
    print("         / ____|                       / __ \                ")
    print("        | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ")
    print("        | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|")
    print("        | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   ")
    print("         \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ")

def win():
    print("          __     __                        ")
    print("          \ \   / /                        ")
    print("           \ \_/ /   __    _    _          ")
    print("            \   /  / _ \  | |  | |         ")
    print("             | |  | ( ) | | |__| |         ")
    print("             |_|   \___/   \____/          ")
    print("          __          __             ")
    print("          \ \        / /             ")
    print("           \ \  /\  / /__  _ __      ")
    print("            \ \/  \/ / _ \| '_ \     ")
    print("             \  /\  / (_) | | | |    ")
    print("              \/  \/ \___/|_| |_|    ")

# 1. cac game choi gan nhat len dau tien NE
def fetch_game() :
    all_saved_games = db.run("SELECT * FROM saved_games")
    input_name = 1 #Input_name column is the second column in saved_games table



    game_option = None
    while True :
        print()
        for i in range(len(all_saved_games)):
            print(f"{i + 1}. {all_saved_games[i][input_name]}")  ##Input
        try :
            game_option = int(input("Select your game: "))
            if game_option < 1 or game_option > len(all_saved_games) :
                print(f"Please enter a number from 1 to {len(all_saved_games)}.")
                continue
            #     print the data of game (result)
            # print(all_saved_games[game_option - 1])

            (money, infected_population, public_dissastisfaction, research_progress, game_turns) = 2, 3, 4, 5, 7
            print(f"+{'':-^16}+{'':-^21}+{'':-^16}+{'':-^17}+{'':-^16}+")

            print(f"|{'MONEY' : ^16}|{'INFECTED POPULATION' : ^21}|{'PUBLIC DISS...' : ^16}|"
                  f"{'RESEARCH PROGRESS' : ^16}|{'GAME TURNS' : ^16}|")

            print(f"|{'':-^16}+{'':-^21}+{'':-^16}+{'':-^17}+{'':-^16}|")

            print(f"|{all_saved_games[game_option - 1][money]:^16}"
                  f"|{all_saved_games[game_option - 1][infected_population] :^21}"
                  f"|{all_saved_games[game_option - 1][public_dissastisfaction] :^16}"
                  f"|{all_saved_games[game_option - 1][research_progress] :^17}"
                  f"|{all_saved_games[game_option - 1][game_turns] :^16}|")

            print(f"+{'':-^16}+{'':-^21}+{'':-^16}+{'':-^17}+{'':-^16}+")

            print("Are you sure about this game ?")
            c = str(input('YES or NO: '))
            if c == 'YES' or c=='yes' or c=='y':
                #return game
                break
            elif c == 'NO':
                continue

        except :
            print(f"Please enter a number from 1 to {len(all_saved_games)}.")

    game_option -= 1

#fetch_game()
