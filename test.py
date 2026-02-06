import pygame
import numpy as np
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




class Food:

    Cell_status = {
        "empty": 0,
        "wall": 1,
        "head" : 2,
        "food": 3,
        "wall_trap ": -31,
        "orientation_trap" : -32, 
        "acceleration_trap" : -33,
        "tail": -2,
        "body" : 22,
        "Portail" :-4
    }

    def __init__(self, the_map, stock_food):
        self.map = the_map
        self.stock_food = stock_food

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






class Snake:
    def __init__(self, the_map):
        self.map = the_map #notre array avec des 0 et des 1
        self.score = 0

        self.head = (self.map.largeur//2, self.map.longueur//2) #démarre au milieu de data
        self.direction = (1,0) #avance vers la droite de base

        #body est une liste de position
        self.body = [[self.head[0],self.head[1]], [self.head[0]-1,self.head[1]] ] #pour l'instant le corps vaut juste la tête et une queue

        self.tail = self.body[-1]

        #changement par un 2 pour la position de base du snake
        self.map.data[self.head[1]][self.head[0]] = 2
        #ajoute une queue
        self.map.data[self.tail[1]][self.tail[0]] = -2
        self.alive = True




    def handle_key(self, key): #récupère l'info sur quelle flèche est pressée
        if key == pygame.K_UP: #true si la flèche vers le haut pressée
            self.direction = (0,-1) #cest inversé c'est normal lol
        if key == pygame.K_DOWN :
            self.direction = (0,1) #true si la flèche vers le bas est pressée

        if key == pygame.K_LEFT :
            self.direction=(-1,0)

        if key == pygame.K_RIGHT:
            self.direction = (1,0)

    def moove(self, the_food): #bouge selon
        x,y = self.head #position initiale de la tête = 2 sur la map

        old_tail = self.body[-1]
        #self.map.data[y][x] = 0 #maintenant c'est un 0 psq on va bouger


        new_x, new_y = x + self.direction[0], y+ self.direction[1] #selon la flèche pressée


        self.head= (new_x, new_y)

        #evolution du snake

        if self.map.data[new_y][new_x]==0:
            self.body.insert(0, self.head) #ajoute la position de la nouvelle tête

            self.body.pop() #enlève l'ancienne position si on n'a rien mangé


        #s'il mange un fruit
        elif self.map.data[new_y][new_x] == 3:
            self.body.insert(0,self.head)

            #on update la food

            the_food.stock_food-=1
            the_food.add_food()

            #on update le score : NEW
            self.score += 1


            #on fait pas le pop cette fois

        # S'il se prend un piège
        elif self.map.data[new_y][new_x] == -3:
            self.score -= 10 # on diminue le score
            
            self.body.insert(0,self.head)
            #on tej la moitié de son corps :


        #si il touche un mur ou son corps, game over
        elif self.map.data[new_y][new_x] == -1 or self.map.data[y][x]==22 or self.map.data[y][x]==-2:
            self.alive = False

            print("game over")


        #modification de la grille :

        self.map.data[new_y][new_x] = 2 #nouvelle position de la tête

        #position de la queue
        tail = self.body[-1]

        self.map.data[tail[1]][tail[0]] = -2
        self.map.data[old_tail[1]][old_tail[0]] = 0 #remet à 0 psq y'a plus la queue

        #remplace toutes les autres position du body par 22

        for i in range(1,len(self.body)-1):

            body_i = self.body[i]

            self.map.data[body_i[1]][body_i[0]] = 22






class Management:
    def __init__(self, the_map,level):
        self.map = the_map
        #met les murs :

        self.map.walls()


        self.snake = Snake(self.map) #créer un snake en fonction de la map initiale

        self.snake_speed = level.snake_speed #vitesse du serpent

        self.stock_food = level.stock_food

        
        




        print("Départ:")
        print(self.map.data)

        self.food = Food(self.map, self.stock_food)
        self.food.add_food() #ajoute une pomme
        print("avec la food")
        print(self.map.data)


    def init_pygame(self):

        pygame.init()
        pygame.display.set_mode((1, 1))

        MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE_EVENT, self.snake_speed)  # 1000 ms


        #tant que running est True, le jeu continue
        running= True
        while running:



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.snake.handle_key(event.key)

                elif event.type == MOVE_EVENT:
                    self.snake.moove(self.food)
                    print("Après touche :")
                    print(self.map.data)

        pygame.quit()




    # def redraw_map(self):
    #     self.init_game
    #     print(self.map.data)





#%% test du management

get_map = Map()
game = Management(get_map)
game.init_pygame()
