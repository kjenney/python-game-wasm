# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///
"""
Main entry point for the Zelda-style Python game.
Compatible with both desktop and WASM (pygbag) deployment.
"""
import asyncio
import pygame
import sys
from character_selection import CharacterSelectionScreen
from game import Game


async def main():
    """Main game loop - async for WASM compatibility."""
    # Initialize Pygame
    pygame.init()

    # Set up the display
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zelda-Style Adventure")

    clock = pygame.time.Clock()
    FPS = 60

    # Character selection phase
    selection_screen = CharacterSelectionScreen(screen)
    selected_character = None

    while selected_character is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            result = selection_screen.handle_event(event)
            if result is not None:
                selected_character = result

        selection_screen.draw()
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Required for WASM compatibility

    # Game phase
    game = Game(screen, selected_character)

    while game.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            game.handle_event(event)

        keys = pygame.key.get_pressed()
        game.update(keys)
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Required for WASM compatibility

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
