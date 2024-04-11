import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep

class Invasion:
    """This clas manges the behavior of the game"""
    def __init__(self):
        """Initializes the game and creates resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()


        self._create_fleet()
        pygame.display.set_caption("Super Space Invaders 2025")
        self.stats = GameStats(self)
        self.bg_color = self.settings.bg_color
    
    def _create_fleet(self):
        """Creates a fleet of aliens"""
        #Make an alien
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.settings.screen_width - (2* alien_width)
        available_space_y = self.settings.screen_height - (3*alien_height) - self.ship.rect.height
        number_aliens_x = available_space_x // (2*alien_width)
        number_rows = available_space_y // (2*alien_height)
        
        #Create the first row
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """start the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_aliens()
            self._update_bullets()
            self._update_screen()
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self.aliens.update()
        self._check_fleet_edges()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
    
    def _ship_hit(self):
        """Responds to an alien hitting the ship"""
        print("Ship Hit!!!")
        self.stats.ships_left -= 1

        #Get rid of any aliens or bullets left on screen
        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        sleep(3)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        #print(f"Total Number of Bullets: {len(self.bullets)}")
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        #check for bullet collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_events(self):
        #Watch for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Checks for keys pressed down
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP: #Checks for keys released
                self._check_keyup_events(event)
            
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
             self._fire_bullet()
        if event.key == pygame.K_q:
             sys.exit()  

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_alllowed:  
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
 
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        #redraw the screen
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

            
        #make the screen visible
        pygame.display.flip()

    def _check_fleet_edges(self):
        """Respond appropriately if any alien reaches the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the aliens and change directions"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == "__main__":
    #Make our game instance
    ai = Invasion()
    ai.run_game()