class Game_Stats:
    '''track stats for the invasion'''

    def __init__(self, ai_game):
        '''initialize statics'''
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        '''initialize statics that can change during the game'''
        self.ships_left = self.settings.ship_limit
        