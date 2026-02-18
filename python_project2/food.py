import random  # Used to generate random positions for food or other game elements


class Food:

    """
        
    This class manages all interactive items placed on the game map
    (such as apples, bombs, walls, etc.)

    It is used for:
    - Identifying empty cells to determine whether an item can be placed.
    - Placing items on the map and updating the game grid accordingly.
    - Handling special placement logic (e.g., bonus food near walls,
    3x3 wall blocks, and portals).

    This class directly interacts with the game map and ensures that
    the grid remains up to date.
    
    """

    # Dictionary that defines the status of each cell in the game grid.
    # Each key represents an element in the game,
    # and each value is a numeric code used to identify that element.
    Cell_status = {
        "empty": 0, # Empty cell
        "wall": 1,  # Wall or obstacle
        "food": 3,  #apple
        "combo_food" : 4, #bonus
        "bomb": -31, # Bomb (causes a penalty)
        "portal_A" :-41, #portal entrance
        "portal_B" : -41 #portal exit
    }



    def __init__(self, the_map, stock_food):

        """
        We initialize the food class with a map reference
        
        the_map (Map): The game grid where items will be placed.
        stock_food (int): The total number of food items required to complete the level. 
        This serves as the win condition; we win
        once this inventory reaches zero.
        """
        self.map = the_map
        self.stock_food = stock_food



    def identify_empty_cells(self):

        "Identify empty cells while ensuring items do not spawn adjacent to walls. and return new random coordinate generated" 

        # get all empty cells from the map
        # store the coordinate of cells whose value is 0
        empty_cells = []

        # Iterate through the grid (excluding outer boundaries to avoid errors)
        for i in range(1, self.map.longueur - 1):
            for j in range(1, self.map.largeur - 1):
                if self.map.data[i][j] == self.Cell_status["empty"]:
                    
                    # Define neighbors: Up, Down, Left, Right
                    neighbors = [
                        self.map.data[i-1][j], self.map.data[i+1][j],
                        self.map.data[i][j-1], self.map.data[i][j+1]
                    ]
                    
                    # Only add cell if NO neighbor is a wall (value 1)
                    if self.Cell_status["wall"] not in neighbors:
                        empty_cells.append((i, j))

        # Return False if no safe cell is found, otherwise return random coordinates
        if not empty_cells:
            return False
            
        return random.choice(empty_cells)



    def add(self, cell_type):

        """
        Identifies available empty cells thanks to identify_empty_cells() and update the map with the choosen object
        Returns True if successful, False if the map is full.

        cell_type: we can choose which item we want to place on the map
        """
        # randomly select a pair of coordinates (i, j) from the list empty_cells
        if self.identify_empty_cells() is False : 
            return False
        
        i, j = self.identify_empty_cells()

        # update the map at the chosen coordinates with the value corresponding to 'cell_type'
        self.map.data[i][j] = self.Cell_status[cell_type]
        return True
    


    def add_food(self):
        """
        Add an apple on the map
        """
        apple_placed = self.add("food")
    


    def add_bomb(self): 
        return self.add("bomb")
    

    
    def place_obstacles(self): #pop_up_bloch_walls

        """
        Generates a 3x3 block of walls at a random location to increase level difficulty.
        """

        i,j = self.identify_empty_cells()

        #Define boundaries to prevent the index to be out of the map
        r_start, r_end = max(0, i - 1), min(self.map.longueur, i + 2)
        c_start, c_end = max(0, j - 1), min(self.map.largeur, j + 2)
        
        #Among the empty cells of the map, ones where no problem of boundaries
        sub_map = self.map.data[r_start:r_end, c_start:c_end]

        #Fill sub_map with O 
        mask = (sub_map == 0) #prevent collision with snake
        sub_map[mask] = self.Cell_status["wall"]
    
    def portail(self): 

        pos_a = self.identify_empty_cells()
        pos_b = self.identify_empty_cells()

        #1 Verify both position are different 
        if pos_a != pos_b : 
            i_a, j_a = pos_a
            i_b, j_b = pos_b
            
            # 2. Mark them on the map
            self.map.data[i_a, j_a] = self.Cell_status["portal_A"]
            self.map.data[i_b, j_b] = self.Cell_status["portal_B"]
            
            # Return coordinates 
            return pos_a, pos_b
    
    def combo_food(self): 

        """
        Spawns a 'combo' food item near walls to create a risk-reward challenge.

        This method prioritizes empty cells adjacent to walls (risky cells). 
        If no wall-adjacent cells are available, it defaults to standard random placement.

        Returns:
            bool: True if placed successfully
        """
        # Filter all currently available empty coordinates
        empty_cells = [
            (i, j)
            for i in range(self.map.longueur)
            for j in range(self.map.largeur)
            if self.map.data[i][j] == self.Cell_status["empty"]
        ]
        #Identify 'risky' cells (empty cells touching at least one wall)
        risky_cells = []

        for i, j in empty_cells:
            # Check closest neighbors (Up, Down, Left, Right)
            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for ni, nj in neighbors:
                # Boundary check: ensure the neighbor is within matrix limits
                if 0 <= ni < self.map.largeur and 0 <= nj < self.map.longueur:
                    #If the neighbors is a wall
                    if self.map.data[ni][nj] == self.Cell_status['wall']:
                        risky_cells.append((i, j))
                        break #Optimization : once we found one, no need verify all neighbors 

        # If risky cells are identified, pick one with random
        if risky_cells:
            i, j = random.choice(risky_cells)
            self.map.data[i][j] = self.Cell_status['combo_food']
        else :
        
            # Otherwise standard placement if no risky cells are available
            return self.add("food")

