# Handles user input. Translates user input depending on said input.

# Movement keys
def handle_keys(user_input):
    if user_input.key =='UP':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT':
        return {'move': (1, 0)}

    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True} # Alt + Enter toggles fullscreen

    elif user_input.key == 'ESCAPE':
        return {'exit': True} # Escape key exits the game

    return {} # No key pressed