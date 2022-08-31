import pygame
import sys

from bullet import Bullet
from settings import Settings
from ship import Ship


class AlienInvasion:
    """info: 1st step: Pygame Window: drawing the game elements
    Overall class to manage game assets and behavior.
    """

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # info: pygame.display.set_mode(size) --> a pygame window
        # info: self.screen --> surface --> redraw by each loop
        # self.screen = pygame.display.set_mode(
        #    size=(self.settings.screen_width, self.settings.screen_height)
        # )

        # info: fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # * set the background color
        # self.bg_color = (230, 230, 230)

        # * create ship
        self.ship = Ship(self)
        # info: create bullets
        self.bullets = pygame.sprite.Group()

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while True:
            # * Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self._update_bullets()

            # * Redraw the screen during each pass through the loop.
            self._update_screen()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # * Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            # info: move the ship to the right
            self.ship.moving_right = True
        # info: move the ship to the left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
