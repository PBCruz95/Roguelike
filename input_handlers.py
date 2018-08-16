# Handles user input. Translates user input depending on said input.

# Movement keys
def handle_keys(user_input):
    key_char = user_input.char

    if user_input.key =='UP' or key_char == 'i':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 'k':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'j':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'u':
        return {'move': (-1, -1)}
    elif key_char == 'o':
        return {'move': (1, -1)}
    elif key_char == 'n':
        return {'move': (-1, 1)}
    elif key_char == '.':
        return{'move': (1, 1)}

    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True} # Alt + Enter toggles fullscreen

    elif user_input.key == 'ESCAPE':
        return {'exit': True} # Escape key exits the game

    return {} # No key pressed