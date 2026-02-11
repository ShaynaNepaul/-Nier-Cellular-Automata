import random

class Food:

    Cell_status = {
        "empty": 0,
        "wall": 1,
        "head" : 2,
        "food": 3,
        "wall_trap": -31,
        "orientation_trap" : -32, 
        "acceleration_trap" : -33,
        "acceleration_zone" : -333,
        "tail": -2,
        "body" : 22,
        "portal_A" :-41, 
        "portal_B" : -41
    }

    def __init__(self, the_map, stock_food):
        self.map = the_map
        self.stock_food = stock_food

    def identify_empty_cells(self):

        "Identifies available empty cells and return new random coordinate generated" 
        # get all empty cells from the map
        # store the coordinate of cells whose value is 0

        empty_cells = [
            (i, j)
            for i in range(self.map.longueur)
            for j in range(self.map.largeur)
            if self.map.data[i][j] == self.Cell_status["empty"]
        ]

        # check whether any cell is available to add something
        if not empty_cells:
            return False
        i, j = random.choice(empty_cells)

        return i,j


    def add(self, cell_type):

        """
        Identifies available empty cells and update the map with the choosen object
        Returns True if successful, False if the map is full.

        :param cell_type: str
        """
        # randomly select a pair of coordinates (i, j) from the list empty_cells
        if self.identify_empty_cells() is False : 
            print("No empty spot on the map")
            return False
        
        i, j = self.identify_empty_cells()

        # update the map at the chosen coordinates with the value corresponding to 'cell_type'
        self.map.data[i][j] = self.Cell_status[cell_type]
        return True

    def add_food(self):
        """
        Add an apple on the map
        Return True whether an apple has been placed 
        """
        apple_placed = self.add("food")
        if apple_placed is True : 
            return True
        
    def add_wall_trap(self): 
        return self.add("wall_trap")
    
    def add_orientation_trap(self): 
        return self.add("orientation_trap")
    
    def acceleration_trap(self):
        return self.add("acceleration_trap")
    
    def pop_up_bloch_walls(self): 

        " Add a 3*3 bloc of walls"

        i,j = self.identify_empty_cells()

        #Define boundaries to prevent the index to be out of the map
        r_start, r_end = max(0, i - 1), min(self.map.longueur, i + 2)
        c_start, c_end = max(0, j - 1), min(self.map.largeur, j + 2)
        
        #Among the empty cells of the map, ones where no problem of boundaries
        sub_map = self.map.data[r_start:r_end, c_start:c_end]

        #Fill sub_map with O 
        mask = (sub_map == 0)
        sub_map[mask] = self.Cell_status["wall"]

    def pop_up_line_wall(self): 
        " Add a full horizontal or vertical line of walls"

        i,j = self.identify_empty_cells()
        param = random.random()

        if param <= 0.5 : 
            # Honrizontal line
            line = self.map.data[i,:]
            mask = (line == 0)
            line[mask] = self.Cell_status["wall"]
        else : 
            #Vertical line
            line = self.map.data[:,j]
            mask = (line == 0)
            line[mask] = self.Cell_status["wall"]

    def pop_up_tunnel_wall(self): 
        " Creates two parallel walls with a path in the middle"
        param = random.random()
        i, j = self.identify_empty_cells()

        if param < 0.5 : 
            orientation = "horizontal"
        else : 
            orientation = "vertical"

        if orientation == "horizontal": 

            line_i = self.map.data[i,:]
            line_i2 = self.map.data[i+2,:]
            mask_i = (line_i == 0)
            mask_i2 = (line_i2 == 0)
            line_i[mask_i] = self.Cell_status["wall"]
            line_i2[mask_i2] = self.Cell_status["wall"]

        else : 
            line_j = self.map.data[:,j]
            line_j2 = self.map.data[:,j+2]
            mask_j = (line_j == 0)
            mask_j2 = (line_j2 == 0)
            line_j[mask_j] = self.Cell_status["wall"]
            line_j2[mask_j2] = self.Cell_status["wall"]
    
    def reduce_map_wall(self): 
        """
        Reduce the size of the map by adding walls with a thickness
        """
        length = self.map.hauteur 
        width = self.map.largeur 
        #Up line
        self.map.data[:5, :] = self.Cell_status["wall"]
        #bottom line
        self.map.data[length-5:, :] = self.Cell_status["wall"]
        #Left 
        self.map.data[:, :5] = self.Cell_status["wall"]
        #Right 
        self.map.data[:, width-5:] = self.Cell_status["wall"]


    def speed_up_zone(self): 
        i,j = self.identify_empty_cells()

        r_start, r_end = max(0, i - 4), min(self.map.longueur, i + 5)
        c_start, c_end = max(0, j - 4), min(self.map.largeur, j + 5)
        
        sub_map = self.map.data[r_start:r_end, c_start:c_end]

        mask = (sub_map == 0)
        sub_map[mask] = self.Cell_status["acceleration_zone"]
        
        # We return the coordinates so the game knows what to delete later
        return (r_start, r_end, c_start, c_end)
    
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
