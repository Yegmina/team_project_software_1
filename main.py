import mariadb
from geopy.distance import geodesic

import Yehor


class Game :


    def __init__(self):
        self.money = 1000000
        self.infected_population = 1 #%
        self.public_dissatisfaction = 20 #%
        self.research_progress = 0 #%
        #self.cure_cost = 30000 #not needed now
        self.game_over = False
        self.game_turn = 0 #counter

    def start(self):
        pass

    def make_choice(self):
        pass

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


#testing
game1 = Game()
print(Yehor.get_airport_coordinates("SA01"))


Yehor.payment_choice(
    game1,
    local_money_needed=50000,
    local_infected_changing=5,
    local_dissatisfaction_changing=0,
    local_research_progress_changing=15,
    local_text="You invested in vaccine research."
)

print(Yehor.distance_between_two(Yehor.get_airport_coordinates("SA01"),Yehor.get_airport_coordinates("SA01")))
