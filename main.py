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
from character_selection import CharacterSelectionScreen, CREATE_CUSTOM_INDEX
from character_creator import run_character_creator
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

    # Main game loop - allows returning to character selection
    keep_playing = True
    while keep_playing:
        # Character selection phase
        selection_screen = CharacterSelectionScreen(screen)
        selected_character_index = None
        custom_character = None

        while selected_character_index is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                result = selection_screen.handle_event(event)
                if result is not None:
                    selected_character_index = result

            selection_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)  # Required for WASM compatibility

        # Handle custom character creation if selected
        if selected_character_index == CREATE_CUSTOM_INDEX:
            custom_character = await run_character_creator(screen)
            if custom_character is None:
                # User cancelled, go back to selection
                selected_character_index = None
                while selected_character_index is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return

                        result = selection_screen.handle_event(event)
                        if result is not None:
                            selected_character_index = result

                    selection_screen.draw()
                    pygame.display.flip()
                    clock.tick(FPS)
                    await asyncio.sleep(0)

        # Game phase - pass character index or custom character
        game = Game(screen, selected_character_index, custom_character=custom_character)

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

        # Check if player wants to return to character selection
        if game.return_to_selection:
            continue  # Loop back to character selection
        else:
            keep_playing = False  # Exit and quit game

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
