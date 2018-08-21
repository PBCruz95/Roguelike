# Handles user input. Translates user input depending on said input.

from game_states import GameStates


def handle_keys(user_input, game_state):
    if user_input:
        if game_state == GameStates.PLAYERS_TURN:
            return handle_player_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keys(user_input)
        elif game_state == GameStates.TARGETING:
            return handle_targeting_keys(user_input)
        elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            return handle_inventory_keys(user_input)
        elif game_state == GameStates.LEVEL_UP:
            return handle_level_up_menu(user_input)
        elif game_state == GameStates.CHARACTER_SCREEN:
            return handle_character_screen(user_input)

    # No key pressed
    return {}

# Targeting keys
def handle_targeting_keys(user_input):
    # Exit the game
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    # No key pressed
    return {}

# Inventory keys
def handle_inventory_keys(user_input):
    # Invalid key
    if not user_input.char:
        return {}

    index = ord(user_input.char) - ord('a') # ord: convert key pressed to an index

    if index >= 0:
        return {'inventory_index': index}

    # Alt+Enter: toggle full screen
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}

    # Exit inventory view   
    elif user_input.key == 'ESCAPE' or user_input.key == 'TAB':
        return {'exit': True}

    # No key pressed
    return {}

# Player turn keys
def handle_player_turn_keys(user_input):
    key_char = user_input.char

    # Movement
    if user_input.key =='UP' or key_char == 'w':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 's':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'a':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1, 1)}
    elif key_char == 'c':
        return{'move': (1, 1)}
    elif key_char == 'x':
        return {'wait': True}

    # Item management
    if key_char == 'f':
        return{'pickup': True}
    elif user_input.key == 'TAB' and user_input.shift:
        return{'drop_inventory': True}
    elif user_input.key == 'TAB':
        return{'show_inventory': True}

    # Take stairs to next level
    elif user_input.key == 'SPACE':
        return {'take_stairs': True}

    # View character stats
    elif user_input.key == 'ALT':
        return {'show_character_screen': True}

    # Alt+Enter: toggle full screen
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}

    # Exit the game
    elif user_input.key == 'ESCAPE':
        return {'exit': True}

    # No key pressed
    return {}

# Player dead keys
def handle_player_dead_keys(user_input):
    key_char = user_input.char

    if key_char == 'i':
        return {'show_inventory': True}

    # Alt+Enter: toggle full screen
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}

    # Exit the game
    elif user_input.key == 'ESCAPE':
        return {'exit': True}

    # No key pressed
    return {}

# Main menu
def handle_main_menu(user_input):
    if user_input:
        key_char = user_input.char

        if user_input.key == 'ENTER' and user_input.alt:
            return {'fullscreen': True}
        elif key_char == 'a':
            return {'new_game': True}
        elif key_char == 'b':
            return {'load_game': True}
        elif key_char == 'c' or user_input.key == 'ESCAPE':
            return {'exit': True}

    return {}

# Level up menu
def handle_level_up_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}

# Charcter stats screen
def handle_character_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}

# Mouse events
def handle_mouse(mouse_event):
    if mouse_event:
        (x, y) = mouse_event.cell

        if mouse_event.button == 'LEFT':
            return {'left_click': (x, y)}
        elif mouse_event.button == 'RIGHT':
            return {'right_click': (x, y)}

    return {}