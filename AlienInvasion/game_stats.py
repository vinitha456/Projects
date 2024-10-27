class GameStats:
    """Track statistics for Alien Invasion."""
    def __init__(self, settings):
        """Initialize statistics for Alien Invasion."""
        self.settings = settings  # Store the settings instance
        self.reset_stats()  # Initialize changing stats

        # Game starts in an inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0  # Initialize the high score

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _end_game(self):
        """handle the end of the game"""
        self.stats.check_high_score(self)
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    def check_high_score(self):
        """Check to see if there is a new high score."""
        if self.score > self.high_score:
            self.high_score = self.score  # Update high score

    def _update_screen(self):
        """Update the images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()  # This will include the high score

        # Make the most recently drawn screen visible
        pygame.display.flip()


