import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng()
import random


class Map:
    def __init__(self):
        self.longueur = 10
        self.largeur = 10
        self.data = np.zeros((self.longueur,self.largeur), dtype=int)

    def walls(self):
        """
        Add walls on the extrimity of the map

        Returns
        -------
        None.

        """
        for i, row in enumerate(self.data) : #récupère la ligne i
            for j,_ in enumerate(row) : #récupère les indices j de la ligne i
                if j==0 or i==0 :
                    self.data[i][j] =1 #ça remplace les murs par la valeur 1
                    self.data[i-1][j-1] =1

class Food(Map): 

    def __init__(self):
        super().__init__()
        self.stock_food = 10

    Cell_status = {
    "empty": 0,
    "wall": 1,
    "food": 3,
    "trap_1": -1,
    "trap_2": -2
}
    def add(self, cell_type):

        empty_cell = [
            (i, j)
            for i in range(self.longueur)
            for j in range(self.longueur)
            if self.data[i][j] == 0
        ]

        i, j = random.choice(empty_cell) #random selection 
        self.data[i][j] = self.Cell_status[cell_type]


#Test 

game_map = Food()

# map avant ajout
print("=== Avant ajout de la food ===")
print(game_map.data)

game_map.walls()

# map après murs mais avant food
print("\n=== Après murs (avant food) ===")
print(game_map.data)

game_map.add("food")

# map après ajout de la food
print("\n=== Après ajout de la food ===")
print(game_map.data)