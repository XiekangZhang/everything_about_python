import sys
import pygame
from ship import Ship
from settings import Settings


class AlienInvasion:
    """1st step: Pygame Window: drawing the game elements
    Overall class to manage game assets and behavior.
    """

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # ! pygame.display.set_mode(size) --> a pygame window
        # ! self.screen --> surface --> redraw by each loop
        self.screen = pygame.display.set_mode(
            size=(self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # * set the background color
        # self.bg_color = (230, 230, 230)

        # * create ship
        self.ship = Ship(self)

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while True:
            # * Watch for keyboard and mouse events.
            self._check_events()

            # * Redraw the screen during each pass through the loop.
            self._update_screen()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # * Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
