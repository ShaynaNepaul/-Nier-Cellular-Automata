import pygame
from map import Map
from food import Food


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
        self.portals = None
        
    


    def handle_key(self, key): #récupère l'info sur quelle flèche est pressée
    
    
        new_directions = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        }
        
        
        
        if key in new_directions:
            new_dir = new_directions[key]
    
            # interdit demi-tour
            if new_dir != (-self.direction[0], -self.direction[1]):
                self.direction = new_dir
                
    def update_portals(self):
        """Cherche les deux portails -41 et les mémorise."""
        if self.portals is None:
            found = []
            for j in range(self.map.longueur):
                for i in range(self.map.largeur):
                    if self.map.data[j][i] == -41:
                        found.append((i, j))
            if len(found) == 2:
                self.portals = found

    def moove(self, the_food): #bouge selon
        """ Movement implementation """
        old_x,old_y = self.head #Initial position of the head on the map
        old_tail = self.body[-1] # Store last tail position to clear it later
        new_x, new_y = old_x + self.direction[0], old_y+ self.direction[1] # new head position according to the arrow pressed
        

        try:
            cell_type = self.map.data[new_y][new_x]   # on LIT la case cible
        except IndexError:
            self.alive = False
            print("Game over il sort de la map")
            return
        
        self.update_portals()
        portals = self.portals if self.portals is not None else []

        
        self.head= (new_x, new_y)

                    
                    
        # --- collision corps ---
        # (22 = corps, -2 = queue)
        if cell_type in (22, -2, 1):
            self.alive = False
            print("game over, collision corps")
            return            


                    
                    
# =========================================================
# PORTAIL : si on marche sur -41
# =========================================================
        if cell_type == -41 and len(portals) == 2:
            (x1, y1), (x2, y2) = portals
        
            # 1) avancer d'une case comme "vide"
            self.body.insert(0, [new_x, new_y])
            self.body.pop()
        
            # 2) téléport vers l'autre centre
            if (new_x, new_y) == (x1, y1):
                new_x, new_y = x2, y2
            else:
                new_x, new_y = x1, y1
        
            # mettre à jour la tête ET le body[0] 
            self.head = (new_x, new_y)
            self.body[0] = self.head
        

        # --- Snake Evolution ---

        else:
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
                
    

        
# =========================================================
# REDRAW COMPLET DU SNAKE SUR LA MAP
# (évite tous les bugs de tête/corps lors de téléport)
# =========================================================
        
        # 1) effacer anciennes traces du snake
        self.map.data[self.map.data == 2] = 0
        self.map.data[self.map.data == 22] = 0
        self.map.data[self.map.data == -2] = 0
        
        # 2) dessiner tête / corps / queue selon self.body
        hx, hy = self.body[0]
        self.map.data[hy][hx] = 2
        
        tx, ty = self.body[-1]
        self.map.data[ty][tx] = -2
        
        for bx, by in self.body[1:-1]:
            self.map.data[by][bx] = 22
        
        # 3) restaurer les portails sans écraser le snake
        snake_cells = {(bx, by) for bx, by in self.body}
        for (px, py) in portals:
            if (px, py) not in snake_cells:
                self.map.data[py][px] = -41
