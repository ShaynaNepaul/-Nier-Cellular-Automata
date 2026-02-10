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
        
        # On initialise food avec un stock par défaut, load_level le mettra à jour
        self.food = Food(self.map, stock_food=0)

        # Propriétés de gestion
        self.current_level = 1
        self.base_move_ms = move_ms 
        self.MOVE_EVENT = pygame.USEREVENT + 1

        # CHARGEMENT DU NIVEAU 1
        self.load_level()

        self.display = Display(self.map, self.snake, gameboard=None, cell_size=cell_size)

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.snake.handle_key(event.key)

                elif event.type == self.MOVE_EVENT:
                    if self.snake.alive:
                        self.snake.moove(self.food)
                        
                        # --- VERIFICATION CHANGEMENT DE NIVEAU ---
                        if self.food.stock_food <= 0:
                            self.current_level += 1
                            # Si load_level renvoie False, c'est qu'il n'y a plus de niveaux
                            if not self.load_level():
                                print("Victoire Totale !")
                                running = False
                    else:
                        running = False

            # Rendu (inchangé)
            self.screen.fill((255, 255, 255))
            self.display.draw_grid(self.screen)
            self.display.border(self.screen)
            self.display.draw_apple(self.screen)
            self.display.draw_snake_body(self.screen)
            self.display.draw_snake_head(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()