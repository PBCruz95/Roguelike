# The game's engine. Captures input and does things with said input.

import tdl
from entity import Entity
from input_handlers import handle_keys
from map_utils import make_map
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255)) # Python 3 doesn't auto truncate division; have to cast result as integer
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', (255, 255, 0))
    entities = [npc, player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True) 

    root_console = tdl.init(screen_width, screen_height, title='Roguelike')
    con = tdl.Console(screen_width, screen_height)

    game_map = tdl.map.Map(map_width, map_height)
    make_map(game_map)

    while not tdl.event.is_window_closed(): # Game loop
        render_all(con, entities, game_map, root_console, screen_width, screen_height, colors)

        tdl.flush() # Present drawing on screen

        clear_all(con, entities) # Erase character before drawing it again. For movement

        for event in tdl.event.get(): # User input
            if event.type == 'KEYDOWN':
                user_input = event
                break
            
        else: # Python feature: put an 'else' after a for loop that only executes if we do not break out of the loop
            user_input = None

        if not user_input: # Return to top of loop
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())
            



if __name__ == '__main__':
    main()