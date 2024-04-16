class Settings:
    """A class to keep track of all the settings in the game"""

    def __init__(self):
        """Initialize the game settings"""
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (31, 31, 31)

        #Ship Settings
        self.ship_speed = 0.75
        self.ship_limit = 3 #lives

        #Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (225, 0, 0)
        self.bullets_alllowed = 3

        #Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 5
        self.fleet_direction = 1 #1 represents right and -1 represents left

        # How Quickly the game soeeds up
        self.speedup_scale = 1.25

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 0.50
        self.bullet_speed = 1.0
        self.alien_speed = 0.50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale