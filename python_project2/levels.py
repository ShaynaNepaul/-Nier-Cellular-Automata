from food import *

LEVELS = {'1': {'stock_apple': 5, 'traps': [], 'speed' : 4, 'nombre_obstacles' : 0},
          '2': {'stock_apple' : 6, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 7, 'nombre_obstacles' : 4},
          '3': {'stock_apple' : 10, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 10, 'nombre_obstacles' : 7},
          '4': {'stock_apple': 10, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 12, 'nombre_obstacles' : 8},
          '5': {'stock_apple': 15, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 20},
}