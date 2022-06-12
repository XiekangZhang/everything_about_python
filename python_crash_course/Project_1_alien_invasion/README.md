# Developing games with PyGame

## main part

- creating screen size to play the game: pygame.display.set_mode(size=())
- setting game name: pygame.display.set_caption()
- using none-stop loop to run the game and using: pygame.event.get(), event.type == pygame.QUIT --> sys.exit() to stop the game
- setting background color: screen.fill(**RGB**)
- updating game windows: pygame.display.flip()

## element part

- drawing the game element: screen.blit(element, element_location)
- pygame treats all game elements like rectangles: screen.get_rect()
