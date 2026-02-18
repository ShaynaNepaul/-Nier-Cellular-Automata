import numpy as np

class Map:
    """
    This class represents the game grid.

    The map is implemented as a 2D numerical matrix (NumPy array) where each cell
    contains an integer value representing its status (empty, wall, snake body, 
    food, bomb, portal, etc.). The cell statuses are updated via the Food and Snake classes.

    Using numerical values is an efficient way to handle: 
    - Collision detection for instance if the snake goes on a cell identified as a wall (1) 
    - Identify the empty cells where an item can be added (with the food class)
    - Manage the snake's path by updating cell states (head, body, tail) as it traverses the map
    """

    def __init__(self):

        """
        Initializes an empty map with the given dimensions.

        Args:
            length (int): The number of rows in the matrix.
            width (int): The number of columns in the matrix.
        """

        self.longueur = 30
        self.largeur = 30
        self.data = np.zeros((self.longueur,self.largeur), dtype=int)

    def walls(self):
        """
        Adds boundary walls to the edges of the map.

        This method iterates through the matrix and sets the value to 1 
        for all cells located on the perimeter.
        """
        for i, row in enumerate(self.data) : #récupère la ligne i
            for j,_ in enumerate(row) : #récupère les indices j de la ligne i
                if j==0 or i==0 :
                    self.data[i][j] =1 #ça remplace les murs par la valeur 1
                    self.data[i-1][j-1] =1