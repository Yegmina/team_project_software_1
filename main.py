import Yehor


class Game :


    def __init__(self):
        self.money = 1000000
        self.infected_population = 1
        self.public_dissatisfaction = 20
        self.research_progress = 0
        self.cure_cost = 30000
        self.game_over = False
        self.game_turn = 0

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


game1 = Game()
Yehor.function()