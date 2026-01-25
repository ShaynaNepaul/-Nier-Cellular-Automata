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



#snake
import pygame
from map import Map

class Snake:
    def __init__(self, the_map):
        self.map = the_map #notre array avec des 0 et des 1
        self.head = (self.map.largeur//2, self.map.longueur//2) #démarre au milieu de data
        self.direction = (1,0) #avance vers la droite de base
        self.snake_speed = 15 #snake speed
        self.alive = True #if the snake is still alive or dead
        self.life_jauge = 100 #Health as percentage
        self.score = 0 #player's current score

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

        x_before, y_before = self.head #before mouvement
        new_x, new_y = x_before + self.direction[0], y_before+ self.direction[1] #selon la flèche pressée #arrival cell's coordinate

        arrival_cell =  self.map.data[new_y][new_x] #arrival cell's value

        #Game Over : update self.alive 
        if arrival_cell in (self.map.Cell_status["wall"], self.map.Cell_status["tail"], self.map.Cell_status["fatal_trap"]): 
            self.alive = False 
        
        #EMPTY CELL : DEFAULT MOUVEMENT
        if arrival_cell == self.map.Cell_status["empty"]:
            self.map.data[y_before][x_before] = self.map.Cell_status["empty"] #maintenant c'est un 0 psq on va bouger
            self.map.data[new_y][new_x] = self.map.Cell_status["head"] #nouvelle position de la tête sur la map
            self.head = (new_x,new_y) 
        
        #FOOD : 
        if arrival_cell == self.map.Cell_status["food"] : 
            self.life_jauge += 10
            self.score += 1

            #MOVE
            self.map.data[y_before][x_before] = self.map.Cell_status["empty"] #maintenant c'est un 0 psq on va bouger
            self.map.data[new_y][new_x] = self.map.Cell_status["head"] #nouvelle position de la tête sur la map
            self.head = (new_x,new_y)

        if arrival_cell == self.map.Cell_status["food_speed"] : 
            self.life_jauge += 10
            self.score += 1
            self.snake_speed += 10

            #MOVE
            self.map.data[y_before][x_before] = self.map.Cell_status["empty"] 
            self.map.data[new_y][new_x] = self.map.Cell_status["head"] 
            self.head = (new_x,new_y)

        #TRAP : lost vitality 
        if arrival_cell == self.map.Cell_status["trap_1"] : 
            self.life_jauge -= 10
            self.score -= 1

            #MOVE
            self.map.data[y_before][x_before] = self.map.Cell_status["empty"] 
            self.map.data[new_y][new_x] = self.map.Cell_status["head"] 
            self.head = (new_x,new_y)
            #game over if life_jauge drops to 0
            if self.life_jauge <= 0:
                self.alive = False

        ##############################

        """

        x,y = self.head #position initiale de la tête = 2 sur la map
        self.map.data[y][x] = 0 #maintenant c'est un 0 psq on va bouger

        new_x, new_y = x + self.direction[0], y+ self.direction[1] #selon la flèche pressée

        self.map.data[new_y][new_x] = 2 #nouvelle position de la tête
    """

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
