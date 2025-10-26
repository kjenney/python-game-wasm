"""
Main game logic and gameplay screen.
"""
import pygame
from characters import get_character_by_index


class Game:
    """Main game class handling gameplay logic."""

    def __init__(self, screen, character_index):
        """
        Initialize the game.

        Args:
            screen: Pygame screen surface
            character_index: Index of the selected character
        """
        self.screen = screen
        self.character = get_character_by_index(character_index)
        self.sprite = self.character.create_sprite()
        self.font = pygame.font.Font(None, 24)
        self.running = True

    def handle_event(self, event):
        """
        Handle game events.

        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self, keys):
        """
        Update game state based on input.

        Args:
            keys: Pygame key state array
        """
        dx = 0
        dy = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.character.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.character.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.character.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.character.speed

        self.character.move(dx, dy, self.screen.get_width(), self.screen.get_height())

    def draw(self):
        """Draw the game screen."""
        # Draw background (grass-like)
        self.screen.fill((34, 139, 34))

        # Draw simple "grass" pattern
        for x in range(0, self.screen.get_width(), 40):
            for y in range(0, self.screen.get_height(), 40):
                pygame.draw.rect(self.screen, (40, 150, 40), (x + 5, y + 5, 10, 10))

        # Draw character
        self.screen.blit(self.sprite, (self.character.x, self.character.y))

        # Draw HUD
        char_info = self.font.render(
            f"Character: {self.character.name} | Use WASD/Arrows to move | ESC to quit",
            True, (255, 255, 255)
        )
        # Draw background for text
        text_bg = pygame.Surface((char_info.get_width() + 20, char_info.get_height() + 10))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(128)
        self.screen.blit(text_bg, (10, 10))
        self.screen.blit(char_info, (20, 15))

    def is_running(self):
        """Check if the game is still running."""
        return self.running
