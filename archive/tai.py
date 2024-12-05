import Colours
def start():
    print("WELCOME TO AIRPORT GAME!! (Press Enter to continue)")
    input()  # Pause for user to press Enter

    input("This game is about managing a disease outbreak...")  # Game description

    print("Rules          : R(1)\n"
          "New Game       : N(2)\n"
          "Continue       : C(3)\n"
          "Quit           : Q(4)\n")


    while True:
        try:
            Start_choice = int(input("Enter your choice: "))
            if Start_choice == 1:
                print(f"RULES: Manage the airport, control the virus spread, and develop a cure.\n"
                      f"\n"
                      f"When closing an airport:\n"
                      + Colours.GREEN + f"Green " + Colours.RESET + f"means it is not infected\n"
                      + Colours.RED + f"Red " + Colours.RESET + f"means the ariport is infected\n"
                      + Colours.STRIKE + f"Strike " + Colours.RESET + f"through means it is closed\n")
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
