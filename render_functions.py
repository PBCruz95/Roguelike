# Functions for drawing and clearing from the screen

from enum import Enum, auto
from game_states import GameStates
from menus import character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, screen_width,
               screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors, game_state):
    if fov_recompute:
        # Map
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))
                game_map.explored[x][y] = True

            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))

    # Entities
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map)

    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

    panel.clear(fg=colors.get('white'), bg=colors.get('black'))

    # Message Log
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x, y, message.text, bg=None, fg=message.color)
        y +=1

    # Health Bar
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

    # Dungeon Depth
    panel.draw_str(1, 3, 'Dungeon Level: {0}'.format(game_map.dungeon_level), fg=colors.get('white'), bg=None)

    # Info Under Mouse
    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))

    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)

    # Inventory management
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it. Press Esc or Tab to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it. Press Esc or Tab to cancel.\n'

        inventory_menu(con, root_console, inventory_title, player, 50, screen_width, screen_height)

    # Level up
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, root_console, 'Level up! Choose a stat to raise:', player, 40, screen_width,
                      screen_height)

    # Character screen
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_console, player, 30, 10, screen_width, screen_height)
        
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, game_map):
    if game_map.fov[entity.x, entity.y] or (entity.stairs and game_map.explored[entity.x][entity.y]):
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_entity(con, entity):
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)