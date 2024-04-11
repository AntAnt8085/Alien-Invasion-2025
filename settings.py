class Settings:
    """A class to keep track of all the settings in the game"""

    def __init__(self):
        """Initialize the game settings"""
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship Settings
        self.ship_speed = 0.75
        self.ship_limit = 3 #lives

        #Bullet Settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (225, 0, 0)
        self.bullets_alllowed = 3

        #Alien Settings
        self.alien_speed = .75
        self.fleet_drop_speed = 15
        self.fleet_direction = 1 #1 represents right and -1 represents left