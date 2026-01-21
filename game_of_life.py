import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng()
import random
import pygame


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
    "queue": -2
}
    def add(self, cell_type):

        empty_cell = [
            (i, j)
            for i in range(self.longueur)
            for j in range(self.longueur)
            if self.data[i][j] == 0
        ]

        i, j = random.choice(empty_cell) #random selection 
        self.data[i][j] = self.Cell_status[cell_type] # regarding the status that we want of the cell, update diff value
        if cell_type == "food": 
            self.stock_food -= 1

#snake
class Snake:
    def __init__(self, the_map):
        self.map = the_map #notre array avec des 0 et des 1

        self.head = (self.map.largeur//2, self.map.longueur//2) #démarre au milieu de data
        self.direction = (1,0) #avance vers la droite de base


        #changement par un 2 pour la position de base du snake
        self.map.data[self.head[0]][self.head[1]] = 2


    def handle_key(self, key): #récupère l'info sur quelle flèche est pressée
        if key == pygame.K_UP: #true si la flèche vers le haut pressée
            self.direction = (0,-1) #cest inversé c'est normal lol
        if key == pygame.K_DOWN :
            self.direction = (0,1) #true si la flèche vers le bas est pressée

        if key == pygame.K_LEFT :
            self.direction=(-1,0)

        if key == pygame.K_RIGHT:
            self.direction = (1,0)

    def moove(self): #bouge selon la flèche pressée
        x,y = self.head #position initiale de la tête = 2 sur la map
        self.map.data[y][x] = 0 #maintenant c'est un 0 psq on va bouger

        new_x, new_y = x + self.direction[0], y+ self.direction[1] #selon la flèche pressée

        self.map.data[new_y][new_x] = 2 #nouvelle position de la tête

#cells pour test si le snake bouge bien

#%% initialisation de la map

get_map = Map()

get_map.walls()



print(get_map.data)

#%% initialisation du snake
snake = Snake(get_map)

#%% apparition du snake

print(get_map.data)

#%% petite fenêtre pour pygame

pygame.init()
pygame.display.set_mode((1, 1))  # fenêtre minimale

#%% recup l'info de la flèc

key_pressed = False

while not key_pressed:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            snake.handle_key(event.key)
            key_pressed = True




#%% moove

snake.moove()

#%% nouvelle data

get_map.data

class Game: 

    """
    Docstring pour Game

    Recuperer la photo 
    """

    # configuration initiale #

    # position ini snake 

    #





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