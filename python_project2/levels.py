from food import *

"""
Configuration dictionary defining the difficulty parameters for each game level.

Each level contains:
- stock_apple (int): The number of apples required to complete the level.
- speed (int): The movement of the snake.
- nombre_obstacles (int): The total count of obstacle blocks to generate with place_obstacles().
- frequence (int): The time interval (in milliseconds) for spawning new bombs.
- bonus (str): indicating if 'combo' food is available ("yes"/"no").

"""
LEVELS = {'1': {'stock_apple': 15, 'speed' : 4, 'nombre_obstacles' : 0, 'frequence_bomb' : 10000, "bonus" : "no", 'portail' : "no"},
          '2': {'stock_apple' : 30, 'speed' : 6, 'nombre_obstacles' : 4, 'frequence_bomb' : 10000, "bonus" : "no", 'portail' : "no"},
          '3': {'stock_apple' : 45, 'speed' : 10, 'nombre_obstacles' : 7, 'frequence_bomb' : 7000, "bonus" : "yes", 'portail' : "yes"},
          
}