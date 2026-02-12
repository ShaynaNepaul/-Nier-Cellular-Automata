from food import *

LEVELS = {'1': {'stock_apple': 5, 'traps': [], 'speed' : 4, 'nombre_obstacles' : 0, 'frequence' : 10000, "bonus" : "no"},
          '2': {'stock_apple' : 6, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 6, 'nombre_obstacles' : 4, 'frequence' : 10000, "bonus" : "no"},
          '3': {'stock_apple' : 15, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 10, 'nombre_obstacles' : 7, 'frequence' : 7000, "bonus" : "yes"},
          '4': {'stock_apple': 20, 'traps' : [Food.pop_up_bloch_walls], 'speed' : 12, 'nombre_obstacles' : 8, 'frequence' : 6000, "bonus" : "yes"},
}