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

                #add continue from this
                return 'continue'
            elif Start_choice == 4:
                print("Goodbye!")
                return 'quit'
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
# design continue game
# def continue_game():

#design game over
def over():
    print("          _____                         ____                 ")
    print("         / ____|                       / __ \                ")
    print("        | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ")
    print("        | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|")
    print("        | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   ")
    print("         \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ")

