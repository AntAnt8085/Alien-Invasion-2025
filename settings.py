class Settings:
    """A class to keep track of all the settings in the game"""

    def __init__(self):
        """Initialize the game settings"""
        #Screen Settings
        
        self.screen_size = input("Would you like large or small screen? ")
        if self.screen_size == "small":
            self.screen_width = 800
            self.screen_height = 600
        if self.screen_size == "large":
            self.screen_width = 1200
            self.screen_height = 800
        
        self.bg_color = (31, 31, 31)

        #Ship Settings
        self.ship_speed = 2
        self.ship_limit = 3 #lives

        #Bullet Settings
        self.bullet_speed = 4
        self.bullet_width = 3
        self.bullet_height = 15 
        self.bullet_color = (225, 0, 0)
        self.bullets_alllowed = 5

        #Alien Settings
        self.alien_speed = 2
        self.fleet_drop_speed = 5
        self.fleet_direction = 1 #1 represents right and -1 represents left

        # How Quickly the game soeeds up
        self.speedup_scale = 1.1
        
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2
        self.bullet_speed = 4
        self.alien_speed = 2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        #Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale        
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)