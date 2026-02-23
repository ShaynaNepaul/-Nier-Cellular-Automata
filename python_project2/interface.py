import numpy as np
import pygame
from food import Food
from food import *
from snake import *
BROWN = (139, 69, 19)

import numpy as np
import pygame
   
class Gameboard:
    """Classe "support" qui stocke des infos globales sur la partie. Ici : l'état game over + le score."""

    def __init__(self, snake):
        """
        - on démarre avec game_over = False
        - on garde un lien vers l'objet snake (pour lire alive/score)
        - on initialise le score avec le score actuel du snake
        """
        
        self.game_over = False # devient True quand la partie est perdue
        self.snake = snake # référence du snake de la partie
        self.score = snake.score # score (au départ, celui du snake)
        self.tot_pomme = 0
        
    def end_game(self):
        """Vérifie si le snake est mort.
        Si oui, on passe game_over à True."""
        
        if not self.snake.alive: # alive == False -> collision
            self.game_over = True


class Display:

    """Classe qui gère tout l'affichage du jeu (grille, serpent, pommes, panneaux, écrans de fin, menu niveaux)."""
    
    def __init__(self, the_map, snake, gameboard, cell_size=20):
        """
        Initialise l'affichage :
        - stocke la map, le snake et le gameboard
        - charge toutes les images
        - prépare les polices et les rectangles (score + sélection de niveaux)
        """
        self.map = the_map
        self.snake = snake
        self.cell_size = cell_size
        self.gameboard = gameboard

        # offset pour centrer la grille dans l'écran
        self.offset_x = 0
        self.offset_y = 0
        
        # paramètres du panneau de score (à droite de la grille)
        self.margin = 60 
        self.panel_w = 260
        self.panel_h = 140

        # polices (titre + valeur)
        self.font_title = pygame.font.SysFont("arial", 32, bold=True) #crée une police en gras pour "score"
        self.font_value = pygame.font.SysFont("arial", 28) #crée une police pour la valeur du score
        
        # Chargement des images 
        # On utilise  convert_alpha() pour garder la transparence 

        self.bg_img = pygame.image.load("total_background.png").convert_alpha()
        self.bg_img.set_alpha(200) #change l'opacité du fond
        
        self.panel_bg_img = pygame.image.load("fond_score_pomme.png").convert_alpha()
        self.panel_bg_img = pygame.transform.smoothscale(self.panel_bg_img, (self.panel_w, self.panel_h))
        
        self.img_game_over = pygame.image.load("game_over.png").convert_alpha()
        self.img_victoire = pygame.image.load("victoire.png").convert_alpha()
        
        self.apple_img = pygame.image.load("apple.png").convert_alpha()
        self.apple_img = pygame.transform.smoothscale(self.apple_img, (self.cell_size+ 3, self.cell_size+3) ) #pour rescale l'image à la taille d'une cellule
        
        self.golden_apple_img = pygame.image.load("golden_apple.png").convert_alpha()
        self.golden_apple_img = pygame.transform.smoothscale(self.golden_apple_img, (self.cell_size, self.cell_size) )
        
        self.bomb_img = pygame.image.load("bomb_mario.png").convert_alpha()
        self.bomb_img = pygame.transform.smoothscale(self.bomb_img, (self.cell_size + 7, self.cell_size+7) ) #pour rescale l'image à la taille d'une cellule
        
        self.snake_head = pygame.image.load("snake_head.png").convert_alpha()
        self.snake_head = pygame.transform.smoothscale(self.snake_head, (self.cell_size, self.cell_size))
        
        self.portail_img = pygame.image.load("portail.jpg").convert_alpha()
        self.portail_img = pygame.transform.smoothscale(self.portail_img, (self.cell_size, self.cell_size))
        
        self.snake_body = pygame.image.load("snake_body.png").convert_alpha()
        self.snake_body = pygame.transform.smoothscale(self.snake_body, (self.cell_size, self.cell_size))
        
        # rotations de la tête pour suivre la direction du snake
        self.snake_head_up    = self.snake_head
        self.snake_head_right = pygame.transform.rotate(self.snake_head, -90)
        self.snake_head_down  = pygame.transform.rotate(self.snake_head, 180)
        self.snake_head_left  = pygame.transform.rotate(self.snake_head, 90)
        
        
        
        #Menu sélection des niveaux (rectangles cliquables)
        self.level_font = pygame.font.SysFont("arial", 24, bold=True)
        self.level_w = 120
        self.level_h = 120
        self.level_gap = 60            
        self.level_left = 150       
        self.level_top = 400          

        # on construit 3 rectangles (2x2)
        w, h, g = self.level_w, self.level_h, self.level_gap
        x0, y0 = self.level_left, self.level_top

        self.level_rects = [
            pygame.Rect(x0,         y0, w, h),        # level 1
            pygame.Rect(x0 + w + g, y0, w, h),        # level 2
            pygame.Rect(x0,         y0 + h + g, w, h)] # level 3
                    
    
    # Outils internes (positions / conversion)
   
        
    def calculate_offset(self, screen):
        """Calcule les offsets (x,y) pour centrer la grille sur l'écran.
        L'écran est en fullscreen et la grille n'a pas forcément la même taille pour tous les ordinateurs."""
        
        screen_w, screen_h = screen.get_size()
        
        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size
        
        self.offset_x = max(0, (screen_w - grid_w) // 2)
        self.offset_y = max(0, (screen_h - grid_h) // 2)
       
        
        
    def cell_to_pixel(self, i, j):
        """Convertit des coordonnées de cellule (i,j) en coordonnées pixels (x,y).
        On ajoute l'offset pour que la grille soit centrée."""

        x = j * self.cell_size + self.offset_x
        y = i * self.cell_size + self.offset_y
        
        return x, y

# Fond + grille


    def draw_grid(self, screen):
        """Dessine les lignes de la grille (quadrillage)."""

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
        """Dessine l'image de fond uniquement sur la zone de la grille (pas sur tout l'écran)."""

        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size

        bg = pygame.transform.smoothscale(self.bg_img, (grid_w, grid_h))
        screen.blit(bg, (self.offset_x, self.offset_y))


# Éléments de jeu (murs / objets / snake)


    def border(self, screen):
        """Dessine les murs (cellules = 1 dans la map)."""

        coords = np.argwhere(self.map.data == 1) #recupère sous forme de liste les coordonnées où on a un 1

        for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             pygame.draw.rect(screen, BROWN, (x, y, self.cell_size, self.cell_size))
             


    def draw_apple(self, screen):
         """Affiche les pommes (cellules = 3 dans la map)."""
             
         coords = np.argwhere(self.map.data == 3) #recupère sous forme de liste les coordonnées où on a un 3   
         
         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             screen.blit(self.apple_img, (x, y)) #blit c'est pour afficher une image
    


    def draw_apple_combo(self, screen):
        """Affiche les pommes dorées (cellules = 4 dans la map)."""
             
        coords = np.argwhere(self.map.data == 4) #recupère sous forme de liste les coordonnées où on a un 3 
         
        for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             screen.blit(self.golden_apple_img, (x, y)) #blit c'est pour afficher une image
             

    
    def draw_trap(self, screen): 
       """Affiche les pièges/bombes (cellules = -31 dans la map)."""
         
       coords = np.argwhere(self.map.data == -31)
       
       for k in coords:

           x, y = self.cell_to_pixel(k[0], k[1])
           screen.blit(self.bomb_img, (x, y))       
       

       
    def draw_portail(self, screen): 
         """Affiche les portails (cellules = -41 dans la map)."""
         
         coords = np.argwhere(self.map.data == -41) #recupère sous forme de liste les coordonnées où on a un 3   
         
         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             screen.blit(self.portail_img, (x, y)) #blit c'est pour afficher une image



    def draw_snake_body(self, screen):
            """Affiche le corps du serpent (cellules = 22)."""
            
            coords = np.argwhere(self.map.data == 22) #recupère sous forme de liste les coordonnées où on a un 1

            for k in coords:

                x, y = self.cell_to_pixel(k[0], k[1])
                screen.blit(self.snake_body, (x, y))


  
    def draw_snake_head(self, screen):
         """Affiche la tête du serpent, avec la bonne rotation selon la direction."""
         
         coords = np.argwhere(self.map.data == 2)
         x, y = self.cell_to_pixel(coords[0][0], coords[0][1])
         
         # selon la direction, on choisit la bonne image tournée
         if self.snake.direction == (-1, 0) :
             screen.blit(self.snake_head_right, (x, y)) #blit c'est pour afficher une image
         
         elif self.snake.direction == (0, 1):
             screen.blit(self.snake_head_up, (x, y))
             
         elif self.snake.direction == (1, 0):
             screen.blit(self.snake_head_left, (x, y))
             
         else: 
             screen.blit(self.snake_head_down, (x, y))

    
    
 # Affichage(score + texte)

    def draw_panel_score(self, screen):
        """Dessine le panneau du score à droite de la grille."""

        # score actuel (on l'affiche tel quel)
        self.score = self.snake.score
        
        # taille de la grille en pixels
        self.grid_w = self.map.largeur * self.cell_size
        self.grid_h = self.map.longueur * self.cell_size
        
        # position du panneau (à droite de la grille)
        x = self.grid_w + self.margin + self.offset_x
        y = self.offset_y  #on descend un peu par rapport au haut de l'écran
        
        panel_rect = pygame.Rect(x, y, self.panel_w, self.panel_h)
        
        # fond du panneau + bordure
        panel_bg = pygame.transform.smoothscale(self.panel_bg_img, (self.panel_w, self.panel_h))
        screen.blit(panel_bg, (x, y))
        pygame.draw.rect(screen, (80, 80, 80), panel_rect, width=3, border_radius=14) #on dessine une bordure par dessus
        
        # texte score
        title = self.font_title.render("Score", True, (139, 69, 19)) #crée une surface avec le texte "Score"
        value = self.font_value.render(str(self.snake.score) +" " + "/" +  " "+  str(self.gameboard.tot_pomme), True, (139, 69, 19)) #pareil avec la valeur

        marge = 18                                          
        screen.blit(title, (x + marge, y + marge))          
        screen.blit(value, (x + 100, y + marge + 40))    



    def draw_game_title(self, screen, title="Snake Game"):
        """Dessine le titre du jeu au-dessus de la grille, avec un contour."""
        
        grid_w = self.map.largeur * self.cell_size
        grid_h = self.map.longueur * self.cell_size
        grid_rect = pygame.Rect(self.offset_x, self.offset_y, grid_w, grid_h)

        # taille de police proportionnelle à la largeur de la grille
        font_size = int(grid_w * 0.2)
        font_size = max(70, min(font_size, 140))
        font = pygame.font.SysFont("trebuchetms", font_size, bold=True)

        cx = grid_rect.centerx
        y = grid_rect.top - 100
        y = max(font_size // 2 + 10, y)

        title_surface = font.render(title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(cx, y))
        screen.blit(title_surface, title_rect)




  # Menu niveaux


    def draw_level_select(self, screen):
        """Dessine les rectangles des niveaux (menu) et effet "hover" : quand la souris passe dessus, le bouton change un peu."""

        mouse_pos = pygame.mouse.get_pos()  # position actuelle de la souris
    
        for i, rect in enumerate(self.level_rects, start=1):
            is_hover = rect.collidepoint(mouse_pos)  # True si la souris est dans le rect
    
            # Effet "enfoncé" : si hover, on dessine un peu plus bas
            draw_rect = rect.move(0, 4) if is_hover else rect
    
            # Couleur différente au survol
            fill = (210, 210, 210) if is_hover else (230, 230, 230)
    
            # Ombre légère (optionnel, effet bouton)
            shadow_rect = rect.move(0, 6)
            pygame.draw.rect(screen, (120, 120, 120), shadow_rect, border_radius=14)
    
            # Rectangle principal
            pygame.draw.rect(screen, fill, draw_rect, border_radius=14)
            pygame.draw.rect(screen, (60, 60, 60), draw_rect, width=3, border_radius=14)
    
            # Texte
            label = self.level_font.render(f"Level {i}", True, (255, 255, 255))
            label_rect = label.get_rect(midtop=(rect.centerx, rect.bottom + 10))
            screen.blit(label, label_rect)
        

    # Écrans de fin (overlay)


    def display_game_over(self, screen): 
        """Affiche l'image "Game Over" au centre avec un voile sombre par-dessus le jeu."""
        
        #calculs des nouvelles dimensions
        target_w = 500
        ratio = target_w / self.img_game_over.get_width()
        target_h = int(self.img_game_over.get_height() * ratio)

        #on crée une version redimensionnée pour l'affichage
        img = pygame.transform.smoothscale(self.img_game_over, (target_w, target_h))
        go_rect = img.get_rect(center=screen.get_rect().center)

        #voile noir transparent pour "assombrir" le fond
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        screen.blit(img, go_rect.topleft)
        


    def display_victoire(self, screen):
        """Affiche l'image "Victory" au centre avec un voile sombre."""
        
        target_w = 500
        ratio = target_w / self.img_victoire.get_width()
        target_h = int(self.img_victoire.get_height() * ratio)
        self.img_victoire = pygame.transform.smoothscale(self.img_victoire, (target_w, target_h))
        
        go_rect = self.img_victoire.get_rect(center=screen.get_rect().center)
        
        
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # noir avec alpha
        screen.blit(overlay, (0, 0))
        screen.blit(self.img_victoire, go_rect.topleft) 