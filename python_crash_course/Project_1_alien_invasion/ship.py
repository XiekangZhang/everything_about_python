import pygame
import os


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

        # info: Load the ship image and get its rect
        self.image = pygame.image.load(
            "python_crash_course/Project_1_alien_invasion/images/ship.bmp"
        )
        self.rect = self.image.get_rect()

        # info: Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self) -> None:
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
