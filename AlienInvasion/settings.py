class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (38, 56, 67)

        # Ship settings
        self.ship_speed_factor = 0.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (236, 194, 94)
        self.bullets_allowed = 3  # Adjust as needed

        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_speed_factor = 1
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.5

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Initialize high score
        self.high_score = 0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 0.5
        # Fleet direction 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
