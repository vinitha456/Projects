import sys
import pygame
from ship import Ship
from settings import Settings
from pygame.sprite import Group
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Class to manage overall game behavior"""
    def __init__(self):
        """Initialize the game and create the game resources"""
        pygame.init()

        self.settings = Settings()  # Save settings as an attribute
        self.stats = GameStats(self.settings)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.sb = Scoreboard(self.screen, self.settings, self.stats)
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self.screen, self.settings)  # Assign ship to self to access it later
        # Store bullets in a group
        self.bullets = Group()
        # Make a group of aliens
        self.aliens = Group()
        # Create the fleet of aliens
        self.create_fleet()
        #make play button
        self.play_button = Button('Play', self)



        # Flag for continuous bullet firing
        self.firing_bullet = False

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self._update_screen()


            if self.stats.game_active:
                self.ship.update()  # Update ship position based on movement flags
                self._update_bullets()
                self.update_aliens()
                self.check_high_score()

            # If the space bar is held down, fire bullets continuously
            if self.firing_bullet:
                self._fire_bullet()

    def _check_events(self):
        """Respond to keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y, self.play_button, self.stats )

    def check_play_button(self, mouse_x, mouse_y, play_button, stats):
        """Start a new game when the Play button is pressed."""
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)

            # Reset the game statistics and scoreboard images
            stats.reset_stats()
            stats.game_active = True

            #reset score to 0
            self.stats.score = 0
            self.sb.prep_score()

            #reset the scoreboard images
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Empty aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # Start firing bullets when the space bar is pressed
            self.firing_bullet = True

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            # Stop firing bullets when the space bar is released
            self.firing_bullet = False


    def _fire_bullet(self):
        """Fire a bullet if limit not reached yet."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and remove old bullets."""
        # Update bullet positions
        self.bullets.update()

        #Check for any bullet alien collisions
        self.check_bullet_alien_collisions()


        # Remove bullets that have disappeared off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        #check for any bullets that have hit aliens
        #if so, get rid of the bullet and the alien

    def check_bullet_alien_collisions(self):
        """Handle bullet-alien collisions and reset score for new levels."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  # Add points for hit aliens
                self.sb.prep_score()  # Update the score display
            self.check_high_score()  # Check if the player got a new high score

        if not self.aliens:  # Check if all aliens have been destroyed
            self.bullets.empty()  # Clear bullets
            self.create_fleet()  # Create a new fleet
            self.settings.increase_speed()  # Increase game speed
            self.stats.level += 1  # Increase level
            self.sb.prep_level()

            # Reset the current score for the new level
            self.stats.score = 0
            self.sb.prep_score()  # Update the score display



    def create_fleet(self):
        """Create a full fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self.settings, self.screen)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = self.get_number_aliens_x(alien_width)
        number_rows = self.get_number_rows(alien.rect.height, self.ship.rect.height)

        # Create the fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def get_number_aliens_x(self, alien_width):
        """Determine the number of aliens that fit in the row"""
        available_space_x = (self.settings.screen_width - (2 * alien_width))
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self.settings, self.screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def get_number_rows(self, alien_height, ship_height):
        """Determine the number of rows of aliens to fit on the screen"""
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self.check_fleet_edges()
        self.aliens.update()

        #look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        #check if any aliens have reached the bottom of the screen
        self.check_aliens_bottom()

    def check_fleet_edges(self):
        """Respond if any aliens have reached the screen edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        """Respond to ship hit by alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            # Update scoreboard
            self.sb.prep_ships()

            # Reset score to 0
            self.stats.score = 0
            self.sb.prep_score()

            # Empty the list of aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()

            # Pause for a moment
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_high_score()  # Display high score

    def check_aliens_bottom(self):
        """Check if any aliens have reached the screen bottom."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # Treat it the same as if the ship got hit
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()  # This will handle ship decrement and score reset
                break

    def check_high_score(self):
        """check to see if there is a new high score"""
        if self.stats.score >= self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

        #redraw all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

            #show high sore if game is over
            self.sb.prep_high_score()


    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Redraw all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #draw the score information
        self.sb.show_score()

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    """Make a game instance and then run the game"""
    ai = AlienInvasion()
    ai.run_game()
