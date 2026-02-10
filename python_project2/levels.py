from food import *


LEVELS = {'1': {'stock_apple': 15, 'traps': [], 'speed' : 5},
          
          '2': {'stock_apple' : 10, 'traps' : [Food.pop_up_bloch_walls, Food.pop_up_line_wall, Food.pop_up_tunnel_wall], 'speed' : 10},
          '3': {'stock_apple' : 8, 'traps' : [Food.pop_up_bloch_walls, Food.pop_up_line_wall, Food.pop_up_tunnel_wall, Food.acceleration_trap], 'speed' : 15},
          '4': {'stock_apple': 5, 'traps' : [Food.pop_up_bloch_walls, Food.pop_up_line_wall, Food.pop_up_tunnel_wall, Food.acceleration_trap], 'speed' : 20},
          '5': {'stock_apple': 5, 'traps' : [Food.pop_up_bloch_walls, Food.pop_up_line_wall, Food.pop_up_tunnel_wall, Food.acceleration_trap], 'speed' : 25},
}