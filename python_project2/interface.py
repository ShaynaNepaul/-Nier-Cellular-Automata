import numpy as np
import pygame
from food import Food
from food import *
from snake import *
BROWN = (139, 69, 19)

import numpy as np
import pygame
   
class Gameboard:

    def __init__(self):
        self.score = 1
        self.game_over = False




class Display:

    def __init__(self, the_map, snake, gameboard, cell_size=20):
        
        self.map = the_map
        self.snake = snake
        self.cell_size = cell_size
        self.gameboard = gameboard
        self.offset_x = 0
        self.offset_y = 0
        
        #pour le rectangle score
        self.margin = 60 #on fixe la taille du rectangle score, et de cb il sera décalé par rapport à la grille
        self.panel_w = 260
        self.panel_h = 140

        self.font_title = pygame.font.SysFont("arial", 32, bold=True) #crée une police en gras pour "score"
        self.font_value = pygame.font.SysFont("arial", 28) #crée une police pour la valeur du score
        
        
        self.bg_img = pygame.image.load("total_background.png").convert_alpha()
        
        
        self.panel_bg_img = pygame.image.load("background.png").convert_alpha()
        self.panel_bg_img = pygame.transform.smoothscale(self.panel_bg_img, (self.panel_w, self.panel_h))
        
        
        self.img_game_over = pygame.image.load("game_over.png").convert_alpha()
        
        
        
        
        self.apple_img = pygame.image.load("apple.png").convert_alpha()
        self.apple_img = pygame.transform.smoothscale(self.apple_img, (self.cell_size, self.cell_size) ) #pour rescale l'image à la taille d'une cellule
        
        self.bomb_img = pygame.image.load("Bomb.png").convert_alpha()
        self.bomb_img = pygame.transform.smoothscale(self.bomb_img, (self.cell_size, self.cell_size) ) #pour rescale l'image à la taille d'une cellule
        
        self.snake_head = pygame.image.load("snake_head.png").convert_alpha()
        self.snake_head = pygame.transform.smoothscale(self.snake_head, (self.cell_size, self.cell_size))
        
        self.portail_img = pygame.image.load("portail.jpg").convert_alpha()
        self.portail_img = pygame.transform.smoothscale(self.portail_img, (self.cell_size*3, self.cell_size*3))
        
        
        self.snake_head_up    = self.snake_head
        self.snake_head_right = pygame.transform.rotate(self.snake_head, -90)
        self.snake_head_down  = pygame.transform.rotate(self.snake_head, 180)
        self.snake_head_left  = pygame.transform.rotate(self.snake_head, 90)
        self.snake_body = pygame.image.load("snake_body.png").convert_alpha()
        self.snake_body = pygame.transform.smoothscale(self.snake_body, (self.cell_size, self.cell_size))
        
        
        
        #pour afficher les rectangles pour les niveaux 
        self.level_font = pygame.font.SysFont("arial", 24, bold=True)

        # paramètres des rectangles
        self.level_w = 120
        self.level_h = 120
        self.level_gap = 60            # espace entre les rectangles
        self.level_left = 180        # marge à gauche
        self.level_top = 400          # marge en haut (à ajuster)

        # on crée les 4 rectangles (2 colonnes x 2 lignes)
        w, h, g = self.level_w, self.level_h, self.level_gap
        x0, y0 = self.level_left, self.level_top

        self.level_rects = [
            pygame.Rect(x0,         y0,         w, h),  # level 1
            pygame.Rect(x0 + w + g, y0,         w, h),  # level 2
            pygame.Rect(x0,         y0 + h + g, w, h),  # level 3
            pygame.Rect(x0 + w + g, y0 + h + g, w, h) ]  # level 4 ]        
        
        
    def display_game_over(self): 
        
        target_w = 500
        ratio = target_w / self.img_game_over.get_width()
        target_h = int(self.img_game_over.get_height() * ratio)
        self.img_game_over = pygame.transform.smoothscale(self.img_game_over, (target_w, target_h))
        
        go_rect = self.img_game_over.get_rect(center=screen.get_rect().center)
        
        
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # noir avec alpha
        screen.blit(overlay, (0, 0))
        screen.blit(self.img_game_over, go_rect.topleft)
        
        
        
        
    def calculate_offset(self, screen):
        
        screen_w, screen_h = screen.get_size()
        
        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size
        
        self.offset_x = max(0, (screen_w - grid_w) // 2)
        self.offset_y = max(0, (screen_h - grid_h) // 2)
       
        
        
    def cell_to_pixel(self, i, j):
        
        x = j * self.cell_size + self.offset_x
        y = i * self.cell_size + self.offset_y
        
        return x, y

    def draw_grid(self, screen):
        # Lignes verticales (colonnes)
        for j in range(self.map.largeur + 1):
            x, y0 = self.cell_to_pixel(0, j)
            _, y1 = self.cell_to_pixel(self.map.longueur, j)
            pygame.draw.line(screen, (200, 200, 200), (x, y0), (x, y1), 1)

        # Lignes horizontales (lignes)
        for i in range(self.map.longueur + 1):
            x0, y = self.cell_to_pixel(i, 0)
            x1, _ = self.cell_to_pixel(i, self.map.largeur)
            pygame.draw.line(screen, (200, 200, 200), (x0, y), (x1, y), 1)


    def draw_grid_background(self, screen):
        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size

    # image redimensionnée à la taille exacte de la grille
        bg = pygame.transform.smoothscale(self.bg_img, (grid_w, grid_h))

    # blit uniquement sur la zone de la grille
        screen.blit(bg, (self.offset_x, self.offset_y))


    def border(self, screen):

         coords = np.argwhere(self.map.data == 1) #recupère sous forme de liste les coordonnées où on a un 1

         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             pygame.draw.rect(screen, BROWN, (x, y, self.cell_size, self.cell_size))
             

    def draw_apple(self, screen):
             
         coords = np.argwhere(self.map.data == 3) #recupère sous forme de liste les coordonnées où on a un 3   
         
         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             screen.blit(self.apple_img, (x, y)) #blit c'est pour afficher une image
             
    
    def draw_trap(self, screen): 
         
       coords1 = np.argwhere(self.map.data == -31)
       coords2 = np.argwhere(self.map.data == -32)
       coords3 = np.argwhere(self.map.data == -33)
         
       coords = np.concatenate((coords1, coords2, coords3))
       
       for k in coords:

           x, y = self.cell_to_pixel(k[0], k[1])
           screen.blit(self.bomb_img, (x, y))       
       
       
    def draw_portail(self, screen): 
         
         coords = np.argwhere(self.map.data == 34) #recupère sous forme de liste les coordonnées où on a un 3   
         
         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             screen.blit(self.portail_img, (x, y)) #blit c'est pour afficher une image
             
             
             
    def draw_snake_head(self, screen):
         
         coords = np.argwhere(self.map.data == 2)
         x, y = self.cell_to_pixel(coords[0][0], coords[0][1])
         
         if self.snake.direction == (1, 0) :
             screen.blit(self.snake_head_right, (x, y)) #blit c'est pour afficher une image
         
         elif self.snake.direction == (0, 1):
             screen.blit(self.snake_head_up, (x, y))
             
         elif self.snake.direction == (-1, 0):
             screen.blit(self.snake_head_left, (x, y))
             
         else: 
             screen.blit(self.snake_head_down, (x, y))             
        


    def draw_snake_body(self, screen):
        
        coords = np.argwhere(self.map.data == 22) #recupère sous forme de liste les coordonnées où on a un 1

        for k in coords:

            x, y = self.cell_to_pixel(k[0], k[1])
            screen.blit(self.snake_body, (x, y))
            

    def draw_panel_score(self, screen):
        
         
        
        self.score = self.gameboard.score
        
        
        #on récupère la taille de la grille : 
        self.grid_w = self.map.largeur * self.cell_size
        self.grid_h = self.map.longueur * self.cell_size
        


        #position du panneau à droite de la grille : 
            
        x = self.grid_w + self.margin + self.offset_x
        y = self.offset_y  #on descend un peu par rapport au haut de l'écran
        
        panel_rect = pygame.Rect(x, y, self.panel_w, self.panel_h)
        
        panel_bg = pygame.transform.smoothscale(self.panel_bg_img, (self.panel_w, self.panel_h))
        screen.blit(panel_bg, (x, y))
        pygame.draw.rect(screen, (80, 80, 80), panel_rect, width=3, border_radius=14) #on dessine une bordure par dessus
        
        title = self.font_title.render("Score", True, (255, 255, 255)) #crée une surface avec le texte "Score"
        value = self.font_value.render(str(self.gameboard.score), True, (255, 255, 255)) #pareil avec la valeur
        
        marge = 18                                          #on crée une marge pour que le texte soit pas collé au rectangle
        screen.blit(title, (x + marge, y + marge))          #on def la position du texte "Score"
        screen.blit(value, (x + marge, y + marge + 55))     # on def la position de la valeur en dessous du "score"
        
        
        
    def draw_text_outline(self, screen, text, font, center,text_color=(255, 255, 255), outline_color=(0, 0, 0), outline_px=4):
    # Contour
        outline = font.render(text, True, outline_color)
        cx, cy = center
        for dx in range(-outline_px, outline_px + 1):
            for dy in range(-outline_px, outline_px + 1):
                if dx != 0 or dy != 0:
                    screen.blit(outline, outline.get_rect(center=(cx + dx, cy + dy)))

    # Texte principal
        main = font.render(text, True, text_color)
        screen.blit(main, main.get_rect(center=center))


    def draw_game_title(self, screen, title="Jeu Snake"):
    # Rect de la grille
        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size
        grid_rect = pygame.Rect(self.offset_x, self.offset_y, grid_w, grid_h)

    # Taille de police : grande, proportionnelle à la largeur de la grille
    # (vous pouvez augmenter les coefficients si vous voulez encore plus gros)
        font_size = int(grid_w * 0.2)          # 20% de la largeur de la grille
        font_size = max(70, min(font_size, 140)) # bornes raisonnables
        font = pygame.font.SysFont("arial", font_size, bold=True)

    # Position : plus haut que maintenant
    # Essayez -80 ou -100 pour le placer plus haut
        cx = grid_rect.centerx
        y = grid_rect.top - 100
        y = max(font_size // 2 + 10, y)

        self.draw_text_outline(screen, title, font, (cx, y), outline_px=5)




    def draw_level_select(self, screen):
        for i, rect in enumerate(self.level_rects, start=1):
        # rectangle (vous pouvez changer les couleurs)
            pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=14)
            pygame.draw.rect(screen, (60, 60, 60), rect, width=3, border_radius=14)

        # texte "Level i" en dessous
            label = self.level_font.render(f"Level {i}", True, (255, 255, 255))
            label_rect = label.get_rect(midtop=(rect.centerx, rect.bottom + 10))
            screen.blit(label, label_rect)

        
        
        
        
        
        
carte = Map()       
pygame.init()    
snake = Snake(carte)
gameboard = Gameboard()
         
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


carte.walls()
carte.data[5][7] = 3
carte.data[4][4] = 2
carte.data[4][5] = 22
carte.data[15][15] = -31
carte.data[22][6] = 34
affichage = Display(carte, snake, gameboard)  


running = True
while running:
    for event in pygame.event.get():  # regarde quels événements se sont produits
        if event.type == pygame.KEYDOWN:  # une touche a été enfoncée
            if event.key == pygame.K_ESCAPE:  # la touche échapp a été enfoncée
                running = False

    screen.fill((170, 220, 170))
    affichage.draw_grid_background(screen)  # remplit l'écran en blanc
    
    affichage.calculate_offset(screen)
    affichage.draw_game_title(screen, "Jeu Snake")
    affichage.draw_level_select(screen)
    affichage.draw_grid(screen)
    affichage.border(screen)
    affichage.draw_apple(screen)
    affichage.draw_snake_head(screen)
    affichage.draw_snake_body(screen)
    affichage.draw_panel_score(screen)
    affichage.draw_trap(screen)
    affichage.draw_portail(screen)
    
    if gameboard.game_over: 
        
        
        affichage.display_game_over()
        
        
    pygame.display.flip()

pygame.quit()      
