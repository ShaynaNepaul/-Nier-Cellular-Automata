from food import *

LEVELS = {'1': {'stock_apple': 5, 'traps': [], 'speed' : 4, 'nombre_obstacles' : 0, 'frequence' : 10000},
          '2': {'stock_apple' : 6, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 7, 'nombre_obstacles' : 4, 'frequence' : 10000},
          '3': {'stock_apple' : 10, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 10, 'nombre_obstacles' : 7, 'frequence' : 8000},
          '4': {'stock_apple': 10, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 12, 'nombre_obstacles' : 8, 'frequence' : 6000},
          '5': {'stock_apple': 15, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 20},
}