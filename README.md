# Nier - Cellular Automata

## Project Structure (OOP Architecture)

The project is organized around several main classes:  

### **Management**
Handles the overall game flow.  

**Main functions:**  
- `load_level()` : load a level  
- `start_level()` : start the level  
- `go_to_menu()` : return to the menu  
- `run()` : execute the main game loop  

---

### **Gameboard**
Manages the board and game logic.  

**Main function:**  
- `end_game()` : end the game  

---

### **Display**
Handles rendering and the user interface.  

**Main functions:**  
- `display_game_over()` : show the game over screen  
- `display_victory()` : show the victory screen  
- `draw_grid()` : display the grid  
- `draw_apple()`, `draw_trap()`, `draw_snake()` : draw game elements  
- `draw_game_title()`, `draw_score()` : display the game title and score  

---

### **Map**
Manages the board and walls.  

**Attributes:**  
- `walls` : stores walls and obstacles  

---

### **Food**
Handles items to collect or avoid.  

**Main functions:**  
- `identify_empty_cell()` : detect an empty cell  
- `add_food()` / `add_trap()` : add food or traps  
- `pop_up_bloc_wall()` : generate temporary obstacles  
- `portail()` : manage teleportation portals  

---

### **Snake**
Handles the snake.  

**Main functions:**  
- `handle_key()` : manage player key inputs  
- `update_portals()` : update position through portals  
- `moove()` : move the snake  

---

## 3️⃣ Overall Functioning

- The **Management** class executes the main game loop.  
- The loop collects player actions, updates the **Snake**, **Map**, and **Food**, and refreshes the display via **Display**.  
- Interactions between classes manage:  
  - Collision of the snake with walls or itself  
  - Food consumption  
  - Interaction with traps and portals  

