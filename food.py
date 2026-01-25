import random
from map import Map


class Food:

    Cell_status = {
        "empty": 0,
        "wall": 1,
        "head" : 2,
        "food": 3,
        "food_speed" : 4,
        "trap_1": -1,
        "fatal_trap" : -3,
        "tail": -2
    }

    def __init__(self, the_map):
        self.map = the_map          
        self.stock_food = 10

    def add(self, cell_type):

        """
        Identifies available empty cells and update the map with the choosen object
        Returns False if the map is full.
        
        :param cell_type: str
        """

        # get all empty cells from the map
        # store the coordinate of cells whose value is 0
        empty_cells = [
            (i, j)
            for i in range(self.map.longueur)
            for j in range(self.map.largeur)
            if self.map.data[i][j] == self.Cell_status["empty"]
        ]

        # check whether any cell is available to add something 
        if not empty_cells:
            return False
        
        # randomly select a pair of coordinates (i, j) from the list of empty cells
        i, j = random.choice(empty_cells)

        # update the map at the chosen coordinates with the value corresponding to 'cell_type'
        self.map.data[i][j] = self.Cell_status[cell_type]

    def add_food(self):
        if self.stock_food > 0 and self.add("food") :
            self.stock_food -= 1
            return True
    
    def add_trap(self, trap_type="trap_1"):
        return self.add(trap_type)
    
    def random_spawn(self):

        # Generate a random float between 0.0 and 1.0
        param = random.random()

        # If the value is less than 0.4 
        if param < 0.4 : 
            self.add_trap()
        
        # If the value is less than 0.8 (both this and first if runs)
        if param < 0.8 : 
            self.add_trap()
        
        # If the value is 0.8 or higher
        else : 
            self.add("fatal_trap")



#Test
game_map = Map()
food = Food(game_map)

game_map.walls()
print(" map ini \n")
print(game_map.data)

print(" spawn \n")
food.random_spawn()
print(game_map.data)

print(" spawn \n")
food.random_spawn()
print(game_map.data)


