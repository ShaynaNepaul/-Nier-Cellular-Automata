from map import Map
from Management import Management

def main():
    game_map = Map()
    game = Management(
        the_map=game_map,
        cell_size=20,
        move_ms=200
    )
    game.run()

if __name__ == "__main__":
    main()