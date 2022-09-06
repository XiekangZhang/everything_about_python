# Developing games with PyGame

## Steps

1. initialize the game's background settings: `pygame.init()`
2. create game window: `screen = pygame.display.set_model((x, y))`
3. set game caption: `pygame.display.set_caption("some_name")`
4. use none-stop loop to run game:

```python
import sys
import pygame

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
```

5. make the most recently drawn screen visible: `pgame.display.flip()`
6. add color into background: `screen.fill((RGB))`
7. (optional) find some [artwork](https://pixabay.com/)
8. add game elements into the main window: _pygame treats all game elements like rectangles_
    1. get the main window `screen = game.screen`
    2. get the main window's rectangle `screen_rect = screen.get_rect()`
    3. load _.bmp_ image `image = pygame.image.load(path_to_bmp)`
    4. get image rectangle `image_rect = image.get_rect()`
    5. locate image into main window: `rect.midbottom = screen_rect.midbottom`
    6. show the image: ``ship.blit()``

## Other useful APIs

- `pygame.KEYDOWN` to check whether a key is pressed or not
- `pygame.K_RIGHT` right arrow key
- `pygame.KEYUP` to check whether a pressed key is released again or not
- `pygame.Rect(x, y, w, h)` to create a rectangle
- `pygame.draw.rect(surface, color, what_to_draw)` to draw the rectangle
- `pygame.sprite.Group()` to create a group of an element, it works like a list
- `bullets.sprites()` returns a list of all sprites in the group _bullets_
- `sprite.groupcollide()` to check whether the elements overlap

## Other remarks

- from bottom to up with y decreases
- The game takes more time to write output to the terminal than it does to draw graphics to the game window

[more API](https://www.pygame.org/docs/)

