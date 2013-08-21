import effects
import classes
import copy

COLOR_PAIRS = ('WU', 'UB', 'BR', 'RG', 'GW', 'WB', 'UR', 'BG', 'RW', 'GU')

def start_game():
    play_again=True
    while play_again:        
        x = classes.Game()
        x.update_battlefield()
        while not any([player.lost for player in x.player]):
            state_clear = x.check_state()
            #Once state_clear returns True (no actions taken during
            #state-based effects), a player gains priority.
            if state_clear:
                if x.prior_player.passed_for_turn:
                    x.resolve_next()
                else:
                    x.priority()
        for player in x.player:
            if player.lost:
                print player.name, 'lost'
        if 'n' in raw_input('Play Again? '):
            play_again = False
    print('Thanks for playing!')
    return x

game = start_game()
