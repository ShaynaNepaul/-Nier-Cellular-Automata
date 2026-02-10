import pygame 
from snake import *
from interface import*
from food import *

class Management:
    def __init__(self, the_map, cell_size=60, move_ms=200):
        pygame.init()

        # Plein écran (0,0) => Pygame prend la résolution de l'écran
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # Jeu
        self.map = the_map
        self.map.walls()

        self.snake = Snake(self.map)
        self.food = Food(self.map,stock_food =2 )
        self.food.add_food()

        # Affichage (sans centrage)
        self.display = Display(self.map, self.snake, gameboard=None, cell_size=cell_size)

        # Timer pour déplacer le snake automatiquement
        self.MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_EVENT, move_ms)

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
                    else:
                        running = False

            # Rendu
            self.screen.fill((255, 255, 255))
            self.display.draw_grid(self.screen)
            self.display.border(self.screen)
            self.display.draw_apple(self.screen)
            self.display.draw_snake_body(self.screen)
            self.display.draw_snake_head(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


get_map = Map()
game = Management(get_map, cell_size=20, move_ms=1000)
game.run()