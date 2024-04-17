import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from Scoreboard import Scoreboard

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

        self.play_button = Button(self, "Play")

        pygame.display.set_caption("ALIENS VS KANYE")
        icon = pygame.image.load("images\icon.png") 
        pygame.display.set_icon(icon)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
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
            if self.stats.game_active:    
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
        
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """Responds to an alien hitting the ship"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        #Get rid of any aliens or bullets left on screen
        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        sleep(.5)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        #check for bullet collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_events(self):
        #Watch for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Checks for keys pressed down
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP: #Checks for keys released
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Hide Mouse Cursor.
            pygame.mouse.set_visible(False)

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and cemter the ship.
            self._create_fleet()
            self.ship.center_ship()
            
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
        
        # Draw the score infomation.
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

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

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()

if __name__ == "__main__":
    #Make our game instance
    ai = Invasion()
    ai.run_game()