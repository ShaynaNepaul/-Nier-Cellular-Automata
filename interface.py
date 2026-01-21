#interface
import numpy as np
import pygame


BROWN = (139, 69, 19)


class Map:
    def __init__(self):
        self.longueur = 100
        self.largeur = 100



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



class Display:

    def __init__(self, the_map, cell_size=10):
        self.map = the_map
        self.cell_size = cell_size

    def cell_to_pixel(self, i, j):
        x = j * self.cell_size
        y = i * self.cell_size
        return x, y

    def draw_grid(self, screen):
        # Lignes verticales (colonnes)
        for j in range(self.map.largeur + 1):
            x, y0 = self.cell_to_pixel(0, j)
            _, y1 = self.cell_to_pixel(self.map.longueur, j)
            pygame.draw.line(screen, (0, 0, 0), (x, y0), (x, y1), 1)

        # Lignes horizontales (lignes)
        for i in range(self.map.longueur + 1):
            x0, y = self.cell_to_pixel(i, 0)
            x1, _ = self.cell_to_pixel(i, self.map.largeur)
            pygame.draw.line(screen, (0, 0, 0), (x0, y), (x1, y), 1)



    def border(self, screen):

         coords = np.argwhere(self.map.data == 1)

         for k in coords:

             x, y = self.cell_to_pixel(k[0], k[1])
             pygame.draw.rect(screen, BROWN, (x, y, self.cell_size, self.cell_size))

#Lignes pour lancer l'affichage de la grille avec pygame mais pour l'instant la bordure fonctionne pas

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
carte = Map()
affichage = Display(carte)

running = True
while running:
    for event in pygame.event.get(): #regarde quels évenements se sont produits (touches enfoncés, déplacement de la souris, ...)
        if event.type == pygame.KEYDOWN:   #une touche a été enfoncée
            if event.key == pygame.K_ESCAPE:   #la touche echap a été enfoncé
                running = False
    screen.fill((255, 255, 255))  # rempli l'écran en blanc


    affichage.draw_grid(screen)
    affichage.border(screen)
    pygame.display.flip()


pygame.quit()
