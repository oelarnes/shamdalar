def output(game, player, main_player_message,
           other_player_message=None):
    if other_player_message==None:
        other_player_message = main_player_message
    if game.player_choice == player:
        print main_player_message
    elif game.player_choice == player.next_player:
        if other_player_message!='':
            print other_player_message
    else:
        print main_player_message
