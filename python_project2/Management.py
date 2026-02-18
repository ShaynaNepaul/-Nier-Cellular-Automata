import pygame
from food import *
from snake import *
from interface import * 
from levels import *
from the_map import Map

class Management:

    """This class connects the classes Food, Snake, Map, Display, Level, Gameboard together and manages :
        - game states (menu, play, game_over, victory)
        - timers (movement, bombs, bonus)
        - event loop (keyboard/mouse)
        - rendering loop"""
        
    
    def __init__(self, the_map, cell_size=60, move_ms=1000):
        
        """Initialize the main controller of the game (window, objects, states, and timers)."""
        
        # Initialise game window
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        
        self.map = the_map
        self.map.walls()                            # place border walls on the grid
        self.snake = Snake(self.map)                # create the snake on the map
        self.gameboard = Gameboard(self.snake)      # stores score + game_over variable
        self.food = Food(self.map, stock_food=0)    #Initialise Food with a default stock, updated by load_level according on the level
        self.display = Display(self.map, self.snake, self.gameboard, cell_size=cell_size)

      
        self.state = "menu" #this variable allows to change from different state of the game: "menu" | "play" | "game_over" | "victoire"
        self.current_level = 1
        
        self.base_move_ms = move_ms 
        self.MOVE_EVENT = pygame.USEREVENT + 1               #Timer for the movement
        self.BOMB_TIMER =  pygame.USEREVENT + 2              #Timer for bombs
        self.FOOD_COMBO_TIMER = pygame.USEREVENT +  3       #Timer for combo
                     
        

        pygame.time.set_timer(self.MOVE_EVENT, 0) # When we are in the menu, we stop the movement timer so the snake doesn't moove


    #======================================
    # Initialization of the current level 
    #======================================

    def load_level(self):
        
        """Apply the parameters of the current level from the LEVELS dictionary.
        This method updates:
        - apple stock to finish the level
        - snake speed (MOVE_EVENT timer)
        - obstacles / bombs / bonus spawning timers"""
        
        
        level_key = str(self.current_level)
        
        # Get parameters of the current level : stock_apple, traps, snake speed
        if level_key in LEVELS:
            datas = LEVELS[level_key]
            
            # 1. Update apple stock
            self.food.stock_food = datas["stock_apple"]
            
            # 2. Update snake speed
            
            new_speed = max(50, self.base_move_ms - (datas["speed"] * 10)) 
            pygame.time.set_timer(self.MOVE_EVENT, new_speed)               

            # 3. Placement of osbtacles
            nb_to_place = datas.get('nombre_obstacles', 0)
            for _ in range(nb_to_place):
                Food.place_obstacles(self.food)
            
            # 4. Place first apple
            self.food.add_food()
            
            #5. # Bomb timer: spawn bombs regularly depending on level frequency
            freq_bomb_apparition = datas["frequence_bomb"]
            pygame.time.set_timer(self.BOMB_TIMER, freq_bomb_apparition)    
            self.food.add_bomb()                                            #we add a bomb at the beginning
            
            # 5. Bonus timer: only if the level enables bonus
            if datas["bonus"] == "yes":
                pygame.time.set_timer(self.FOOD_COMBO_TIMER, 30000) #every 30 seconds
                self.food.combo_food()
                
            #BPlacement of portail only if the level enables it
            if datas["portail"] == "yes":
                self.food.portail()
                self.snake.portals = None


            # IMPORTANT: force the snake to re-scan portal positions
            self.snake.portals = None
        else:
            return False # no more levels available
        return True
    


    def start_level(self, level_num):
        """Start a level from the menu.
        We reset the map / snake / food so nothing from the previous run remains
        (old apples, bombs, obstacles, etc.)."""

        
        self.current_level = level_num

        # Reset the map grid, then rebuild the borders
        self.map.data[:, :] = 0
        self.map.walls()

        # Create fresh snake + food
        self.snake = Snake(self.map)
        self.food = Food(self.map, stock_food=0)
        
        # Gameboard must reference the new snake
        self.gameboard.snake = self.snake
        self.gameboard.game_over = False
        
        # Update display references 
        self.display.map = self.map
        self.display.snake = self.snake

        # Load current level parameters and switch state to play
        self.load_level()
        self.state = "play"


    def go_to_menu(self):
        """Return to the menu state. We also stop the movement timer and reset the game_over variable."""

        
        self.state = "menu"                                
        pygame.time.set_timer(self.MOVE_EVENT, 0)   # disable movement in menu   
        self.gameboard.game_over = False           



    def run(self):
        """Main game loop. It manages :
                - pygame events (keyboard, mouse, timers)
                - game state transitions (menu/play/game_over/victory)
                - drawing (rendering once per frame) """

        
        running = True
        while running:
            
            #===========================#
            # EVENTS 
            #===========================#
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:           # Window close
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   # ESC: quit the game
                    running = False
            
                if self.state == "game_over":   #switch to game over state
                  
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      # Click to return to menu
                      self.go_to_menu()  # ignore other events in this state
                    continue
                      
                if self.state == "victoire": ## VICTORY state
                                                          
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.go_to_menu()
                    
                    continue
                
                #===========================#
                # MENU 
                #===========================#
                
                if self.state == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click: check which level rectangle was clicked
                        mouse_pos = event.pos
                        for level_num, rect in enumerate(self.display.level_rects, start=1):
                            if rect.collidepoint(mouse_pos):
                                self.start_level(level_num)  #launch the level
                                break

                #===========================#
                # JEU
                #===========================#
                
                if self.state == "play":
                    if event.type == pygame.KEYDOWN:            # Keyboard arrows: update snake direction
                        self.snake.handle_key(event.key)
                            
                    if event.type == self.MOVE_EVENT:           # Movement tick
                    
                        self.snake.moove(self.food)                     # 1) Move snake (may set snake.alive to False)
                        self.gameboard.score = self.snake.score         # Keep score synced for Display
                                    
                        self.gameboard.end_game()                       # 2) Check game over after the move
                            
                                   
                        if self.gameboard.game_over:                    # 3) If dead: stop movement and switch state
                            self.state = "game_over"
                            pygame.time.set_timer(self.MOVE_EVENT, 0)
                            continue
                            
                        if self.food.stock_food <= 0:                   # 4) Victory: if no apples left to eat
                            self.state = "victoire"
                            pygame.time.set_timer(self.MOVE_EVENT, 0)

                    if event.type == self.BOMB_TIMER:                   # Bomb spawn tick
                        self.food.add_bomb() 
                        

                    if event.type == self.FOOD_COMBO_TIMER :            # Bonus spawn tick
                        self.food.combo_food()
                                            


            #===========================#
            # Affichage
            #===========================#
            
            
            self.screen.fill((170, 220, 170))
            self.display.calculate_offset(self.screen)          # Center the grid
            
            self.display.draw_grid_background(self.screen)      # Background + grid
            self.display.draw_grid(self.screen)
            
            # Game elements
            
            self.display.border(self.screen)
            self.display.draw_apple(self.screen)
            self.display.draw_snake_body(self.screen)
            self.display.draw_snake_head(self.screen)
            
            self.display.draw_trap(self.screen)
            self.display.draw_portail(self.screen) 
            self.display.draw_apple_combo(self.screen)
            
            self.display.draw_level_select(self.screen)
            self.display.draw_panel_score(self.screen)
            self.display.draw_level_select(self.screen)
            self.display.draw_game_title(self.screen)
        
            if self.gameboard.game_over: 
                    
                    self.display.display_game_over(self.screen)
                    
            if self.state == "victoire": 

                self.display.display_victoire(self.screen)
                
    
            pygame.display.flip()
            self.clock.tick(60)
    
        pygame.quit() 
    
     



