import pygame
from map import Map
from food import Food
from interface import Display

class Snake:
    def __init__(self, the_map):
        self.map = the_map #map initialization with only 0 and 1
        self.score = 0
        self.head = (self.map.largeur//2, self.map.longueur//2) #start in the middle of the map
        self.direction = (1,0) # Initial movement: moving right

        #body is a list of coordinates [x,y] for each part of the body
        self.body = [[self.head[0],self.head[1]], [self.head[0]-1,self.head[1]] ] # Initialy body consists of the head and one tail segment behind it
        self.tail = self.body[-1]

        #Update map : 2 represents the head
        self.map.data[self.head[1]][self.head[0]] = 2
        # Update map: -2 represents the tail
        self.map.data[self.tail[1]][self.tail[0]] = -2
        self.alive = True


    def handle_key(self, key): 
        # Get info on which arrow key is pressed
        if key == pygame.K_UP: #true if up arrow is pressed
            self.direction = (0,-1) #cest inversé c'est normal lol
        if key == pygame.K_DOWN :
            self.direction = (0,1) #true if down arrow is pressed

        if key == pygame.K_LEFT :
            self.direction=(-1,0)

        if key == pygame.K_RIGHT:
            self.direction = (1,0)

    def moove(self, the_food): #bouge selon
        """ Movement implementation """
        x,y = self.head #Initial position of the head on the map
        old_tail = self.body[-1] # Store last tail position to clear it later

        new_x, new_y = x + self.direction[0], y+ self.direction[1] # new head position according to the arrow pressed
        self.head= (new_x, new_y)

        # --- Snake Evolution ---

        # Case 0: Empty space
        if self.map.data[new_y][new_x]==0:
            self.body.insert(0, self.head) # Add new head at the first position in body with new tile coordinates
            self.body.pop() # Remove old tail

        # Case 3: Food
        elif self.map.data[new_y][new_x] == 3:
            self.body.insert(0,self.head) # Add new head (no pop = growth of the snake)
            the_food.stock_food-=1 #Update food storage
            the_food.add_food() # Add an apple right after eating one
            self.score += 1 # Update score

        # Case -3: Trap 
        elif self.map.data[new_y][new_x] == -3:
            self.score -= 10 # Decrease the score 
            self.body.insert(0,self.head)
            #on tej la moitié de son corps :


        # Case: Wall (1) or Self-collision (22 or -2)
        elif self.map.data[new_y][new_x] == -1 or self.map.data[y][x]==22 or self.map.data[y][x]==-2:
            self.alive = False
            print("game over")


        # --- MAP RENDERING UPDATE ---

        self.map.data[new_y][new_x] = 2 # New position of the head
        tail = self.body[-1] # Position of the tail

        self.map.data[tail[1]][tail[0]] = -2 #New position of the tail
        self.map.data[old_tail[1]][old_tail[0]] = 0 # Clear the old tail position

        # Replace other positions of the body by 22

        for i in range(1,len(self.body)-1):

            body_i = self.body[i]

            self.map.data[body_i[1]][body_i[0]] = 22
