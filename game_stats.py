import ast

class GameStats():
    """Track stats for the game."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        
        self.file_name = "Highscore.txt"

        # Look for alines hitting the bottom of the screen.
        self.game_active = False
        
        # High score should never be reset.
        self.high_score = self.load_highscore("Highscore.txt")
        
        try:
            values = ast.literal_eval(self.load_highscore(self.file_name))
        except:
            values = 0
    
    def save_highscore(self, highscore, filename):
        """Save the highscore in a seperate file."""
        with open(filename, 'w') as f:
            f.write(highscore)
                
    def load_highscore(self, filename):
        """Load the highscore from a seperate file."""
        with open(filename, 'r') as f:
            read = f.read()
        return read

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
