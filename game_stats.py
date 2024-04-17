class GameStats:
    """Track stats for the game"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        #Look for alines hitting the bottom of the screen.
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
