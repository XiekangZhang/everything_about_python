import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting position.

        Args:
            ai_game (_type_): _description_
        """

        # info: Pygame treats all game elements like rectangles
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings

        # info: Load the ship image and get its rect
        self.image = pygame.image.load(
            "python_crash_course/Project_1_alien_invasion/images/ship.bmp"
        )
        self.rect = self.image.get_rect()

        # info: Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # info: Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self) -> None:
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self) -> None:
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right + (self.rect.right - self.rect.left) / 2:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > - (self.rect.right - self.rect.left) / 2:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
