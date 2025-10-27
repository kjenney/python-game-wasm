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

# Import platform for WASM-specific functionality
if sys.platform == "emscripten":
    import platform


def restore_canvas_focus():
    """
    Restore focus to the pygame canvas.
    This is needed on WASM/mobile to ensure mouse/touch events are captured
    after focus has been lost (e.g., after using HTML input elements).
    """
    if sys.platform == "emscripten":
        try:
            # Try to focus the canvas element
            canvas = platform.window.document.getElementById("canvas")
            if canvas:
                canvas.focus()
            # Also focus the window for good measure
            platform.window.focus()
        except Exception as e:
            print(f"Failed to restore canvas focus: {e}")


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
        # Ensure canvas has focus for mouse/touch events
        restore_canvas_focus()

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
        # Loop until we have a valid character (either custom or preset)
        while selected_character_index == CREATE_CUSTOM_INDEX and custom_character is None:
            custom_character = await run_character_creator(screen)
            # Restore canvas focus after character creator
            restore_canvas_focus()

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
                # Loop will check if selected_character_index is CREATE_CUSTOM_INDEX again

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
