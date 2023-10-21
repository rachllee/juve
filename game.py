import random
class Game:

    def __init__(self, x, y, tutorial):
        self.SCREEN_WIDTH = 20
        self.SCREEN_HEIGHT = 10
        self.TUTORIAL = True
        self.RHAND = [x,y]
        self.LIST_OF_FRUITS = []
        self.score = 0
        self.fruit = []

    # Function to generate a random fruit at the top of the screen
    def create_fruits(self, num):
        for i in range(num/2):
            self.LIST_OF_FRUITS.append([self.WIDTH, self.HEIGHT, 5])
        for i in range(num/2):
            self.LIST_OF_FRUITS.append([self.WIDTH, self.HEIGHT, 4])


    # Function to move and display the "fruits"
    def move_fruits(self):
        for fruit in self.fruits:
            fruit[1] -= 1

    # Function to check if the user hits a fruit
    def check_hit(self, hand, fruit):
        hand_x = hand[0]
        hand_y = hand[1]
        fruit_x = fruit[0]
        fruit_y = fruit[1]
        fruit_r = fruit[2]
        if fruit_x - fruit_r <= hand_x <= fruit_x + fruit_r and fruit_y - fruit_r <= hand_y <= fruit_y + fruit_r:
            return True
        return False
    
    def update_game_tutorial(self, x):
        if self.check_hit(x, 9):
            self.fruits = [fruit for fruit in self.fruits if fruit['y'] != 9]
            self.score += 1
    
