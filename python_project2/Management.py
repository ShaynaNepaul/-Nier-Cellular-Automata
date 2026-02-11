import pygame
from food import *
from snake import *
from interface import * 
from levels import *


class Management:
    
    def __init__(self, the_map, cell_size=60, move_ms=1000):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.map = the_map
        self.map.walls()
        self.snake = Snake(self.map)
        
        self.gameboard = Gameboard(self.snake)
        
        
        # On initialise food avec un stock par défaut, load_level le mettra à jour
        self.food = Food(self.map, stock_food=0)

        # Propriétés de gestion
        self.state = "menu"
        self.current_level = 1
        self.base_move_ms = move_ms 
        self.MOVE_EVENT = pygame.USEREVENT + 1

        pygame.time.set_timer(self.MOVE_EVENT, 0) #on met le timer à 0 quand on est dans le menu

        # CHARGEMENT DU NIVEAU 1
        #self.load_level() on veut choisir au clic

        self.display = Display(self.map, self.snake, self.gameboard, cell_size=cell_size)

    def load_level(self):
        """ Applique les paramètres du niveau actuel depuis le dictionnaire LEVELS """
        level_key = str(self.current_level)
        
        if level_key in LEVELS:
            datas = LEVELS[level_key]
            
            # 1. Mise à jour du stock de nourriture
            self.food.stock_food = datas["stock_apple"]
            
            # 2. Mise à jour de la vitesse (on modifie le timer)
            # On peut utiliser la valeur 'speed' de ton dict pour ajuster le move_ms
            # Plus 'speed' est haut, plus l'intervalle est court
            new_speed = max(50, self.base_move_ms - (datas["speed"] * 10)) 
            pygame.time.set_timer(self.MOVE_EVENT, new_speed)
            
            # 3. Placement des pièges du niveau
            for trap_func in datas["traps"]:
                trap_func(self.food)
            
            # 4. On place la première pomme
            self.food.add_food()
            print(f"Niveau {self.current_level} lancé !")
        else:
            return False # Plus de niveaux
        return True
    


    def start_level(self, level_num):
        
        self.current_level = level_num

    # reset de la carte/serpent/nourriture pour éviter pièges/pommes restent
        self.map.data[:, :] = 0
        self.map.walls()

        self.snake = Snake(self.map)
        self.food = Food(self.map, stock_food=0)
        self.gameboard.snake = self.snake
        self.gameboard.game_over = False
    # reset les références dans l'affichage
        self.display.map = self.map
        self.display.snake = self.snake

        self.load_level()
        self.state = "play"




    def go_to_menu(self):
        self.state = "menu"                                # repasse en état menu
        pygame.time.set_timer(self.MOVE_EVENT, 0)         # interdit les mouvements
        self.gameboard.game_over = False           




    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
                if self.state == "game_over":
                  self.display.display_game_over(self.screen)
                                                    
                  if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                      self.go_to_menu()
                  
                      
                if self.state == "victoire":
                    self.display.display_victory(self.screen)
                                                          
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.go_to_menu()
                
                    
                      
            # menu
                if self.state == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        for level_num, rect in enumerate(self.display.level_rects, start=1):
                            if rect.collidepoint(mouse_pos):
                                self.start_level(level_num)
                                break
                    continue

# Jeu
                if self.state == "play":
                    if event.type == pygame.KEYDOWN:
                        self.snake.handle_key(event.key)
                            
                    if event.type == self.MOVE_EVENT:
                                    # 1) on fait avancer (peut rendre alive=False)
                        self.snake.moove(self.food)
                            
                                    # 2) on met à jour game_over juste après
                        self.gameboard.end_game()
                            
                                    # 3) si game over : stop mouvement + état game_over
                        if self.gameboard.game_over:
                            self.state = "game_over"
                            pygame.time.set_timer(self.MOVE_EVENT, 0)
                            continue
                            
                                    # 4) sinon, fin de niveau
                        if self.food.stock_food <= 0:
                           
                            self.state = "victoire"
                            pygame.time.set_timer(self.MOVE_EVENT, 0)
                            
                    


                                                


        # Affichage
            self.screen.fill((170, 220, 170))
            self.display.calculate_offset(self.screen)
            self.display.draw_grid_background(self.screen)
            self.display.draw_grid(self.screen)
            self.display.draw_level_select(self.screen)
            self.display.border(self.screen)
            self.display.draw_apple(self.screen)
            self.display.draw_snake_body(self.screen)
            self.display.draw_snake_head(self.screen)
            self.display.draw_game_title(self.screen)
            self.display.draw_level_select(self.screen)
            self.display.draw_panel_score(self.screen)
            self.display.draw_trap(self.screen)
            self.display.draw_portail(self.screen) 
            if self.gameboard.game_over: 
                    
                    
                    self.display.display_game_over(self.screen)
            
    
            pygame.display.flip()
            self.clock.tick(60)
    
        pygame.quit() 
    
     



