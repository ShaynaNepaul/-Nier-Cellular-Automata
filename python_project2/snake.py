import pygame
from the_map import Map
from food import Food


class Snake:

    """
    This class manages the snake's state, movement, and interaction logic.
    It is used for:
    - Manage the snake's parts (head, body segments) displacement 
    - Process movement and input : Handling directional changes and 
      preventing 180-degree maneuvers 
    - Manage collision events : Detecting interactions with food (growth), 
      traps (scoring penalties), and portals (teleportation), and collision with tail and wall (death).
    - Update in real time the snake position on the map by placing numerical values (2, 22, -2) on the grid 
    """

    def __init__(self, the_map):
        self.map = the_map # Map initialization with only 0 and 1
        self.score = 0 # Initialization of the score 
        
        #initializing snake
        self.head = (self.map.largeur//2, self.map.longueur//2) # Spawn snake in the center of the grid
        self.direction = (1,0) # Initial movement: Right

        #body is a list of coordinates [x,y] for each part of the body
        self.body = [[self.head[0],self.head[1]], [self.head[0]-1,self.head[1]] ] # Initialy body consists of the head and one tail segment behind it
        self.tail = self.body[-1]  #tail of the snake

        # Initialize head (2) and tail (22) on the map
        self.map.data[self.head[1]][self.head[0]] = 2
        self.map.data[self.tail[1]][self.tail[0]] = 22
        
        # Snake status 
        self.alive = True
        
        #initialization portal status
        self.portals = None
        
        
        
    def handle_key(self, key): 
    
        """
        Keyboard input from the player to change the direction of the snake. Prevent 180-degre mouvements. 
        
        key : The Pygame key (e.g., pygame.K_UP) received from the event loop.
        """

        #the player can give "Up, Down, Right, Left" direction to the snake
        new_directions = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        } #link a key pressed to the direction of the snake
        
        
        if key in new_directions: #test to see if the key pressed is not already the current direction
            new_dir = new_directions[key]            
            if new_dir != (-self.direction[0], -self.direction[1]): # Prevent the snake from reversing directly into itself
                self.direction = new_dir 


                
    def update_portals(self):
        """Locates and store the coordinates of the portal pair on the map."""

        if self.portals is None: #since we didnt locate already the portal, we try to find one
            found = []
            for j in range(self.map.longueur):
                for i in range(self.map.largeur):
                    if self.map.data[j][i] == -41: #location of portals
                        found.append((i, j))
            if len(found) == 2: #prevent error if there is more than 2 portals
                self.portals = found







    def moove(self, the_food): 
        """ Movement implementation and handles interactions with food, traps, and portals """

        old_x,old_y = self.head #Initial position of the head on the map
        #old_tail = self.body[-1] # Store last tail position to clear it later
        new_x, new_y = old_x + self.direction[0], old_y+ self.direction[1] # new head position according to the arrow pressed
        
        #test to see boundaries of the map : error code if the snake goes out
        try:
            cell_type = self.map.data[new_y][new_x]   # read the number on the case targeted
        except IndexError:
            self.alive = False
            return
        
        
        #take position of the portals
        self.update_portals()
        portals = self.portals if self.portals is not None else []

        #update the new position of the head
        self.head= (new_x, new_y)

                    
                    
# Collision detection: Walls (1), body (22) 
        if cell_type in (22, 1):
            self.alive = False
            return            

# PORTAL LOGIC 
        if cell_type == -41 and len(portals) == 2:
            (x1, y1), (x2, y2) = portals
        
            # Mooving on the portal cell (as a normal cell)
            self.body.insert(0, [new_x, new_y])
            self.body.pop()
        
            # teleport to the other portal
            if (new_x, new_y) == (x1, y1):
                new_x, new_y = x2, y2
            else:
                new_x, new_y = x1, y1
         
            self.head = (new_x, new_y) #update snake and body
            self.body[0] = self.head
        

# STANDARD MOVEMENT

        else:
            # Case 0: Empty space
            if self.map.data[new_y][new_x]==0:
                self.body.insert(0, self.head) # Add new head at the first position in body with new tile coordinates
                self.body.pop() # Remove old tail
                
                
#Item interaction    
            # Cell 3: Food
            elif self.map.data[new_y][new_x] == 3:
                self.body.insert(0,self.head) # Add new head (no pop = growth of the snake)
                the_food.stock_food-=1 #Update food storage
                the_food.add_food() # Add an apple right after eating one
                self.score += 1 # Update score
    
            # Cell -31: Trap 
            elif self.map.data[new_y][new_x] == -31:
                self.map.data[new_y][new_x] = 0
                self.body.insert(0, self.head)
                self.body.pop()
                self.score -= 10 # Decrease the score 

            #Cell 4 : Combo food
            elif self.map.data[new_y][new_x] == 4:
                self.body.insert(0,self.head)
                self.score += 5 #incerease score

# --- MAP REFRESH and redraw snake
        
        #Clear snake segments from the map to prevent residual body on the map
        self.map.data[self.map.data == 2] = 0
        self.map.data[self.map.data == 22] = 0
        
        # Write current snake positions back to the map according to self.body
        # which contains current position 
        # of the snake on the map
        head_x, head_y = self.body[0]
        self.map.data[head_y][head_x] = 2 # Head
        
 
        
        for body_x, body_y in self.body[1:]:
            self.map.data[body_y][body_x] = 22 # Body segments
        
        # Restore portal visuals if they aren't covered by the snake's body 
        snake_cells = {(body_x, body_y) for body_x, body_y in self.body}
        for (portal_x, portal_y) in portals:
            if (portal_x, portal_y) not in snake_cells:
                self.map.data[portal_y][portal_x] = -41
