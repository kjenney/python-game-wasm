"""
Main game logic and gameplay screen.
"""
import pygame
import math
from characters import get_character_by_index


class Game:
    """Main game class handling gameplay logic."""

    def __init__(self, screen, character_index, custom_character=None):
        """
        Initialize the game.

        Args:
            screen: Pygame screen surface
            character_index: Index of the selected character (0-2)
            custom_character: Optional custom Character object (overrides character_index)
        """
        self.screen = screen
        # Use custom character if provided, otherwise get by index
        if custom_character is not None:
            self.character = custom_character
        else:
            self.character = get_character_by_index(character_index)
        self.sprite = self.character.create_sprite()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.return_to_selection = False  # Flag to return to character selection

        # Click-to-move state
        self.target_pos = None  # Target position for click-to-move
        self.target_marker_timer = 0  # Timer for target marker animation

    def handle_event(self, event):
        """
        Handle game events.

        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_b:
                # Return to character selection
                self.return_to_selection = True
                self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Set target position for click-to-move
                self.target_pos = event.pos
                self.target_marker_timer = 60  # Show marker for 60 frames (1 second at 60 FPS)

    def update(self, keys):
        """
        Update game state based on input.

        Args:
            keys: Pygame key state array
        """
        dx = 0
        dy = 0

        # Keyboard movement (takes priority over click-to-move)
        keyboard_input = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.character.speed
            keyboard_input = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.character.speed
            keyboard_input = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.character.speed
            keyboard_input = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.character.speed
            keyboard_input = True

        # If keyboard input is active, cancel click-to-move
        if keyboard_input:
            self.target_pos = None
        # Otherwise, handle click-to-move
        elif self.target_pos:
            # Calculate direction to target
            char_center_x = self.character.x + self.character.size // 2
            char_center_y = self.character.y + self.character.size // 2
            target_x, target_y = self.target_pos

            # Calculate distance
            dist_x = target_x - char_center_x
            dist_y = target_y - char_center_y
            distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

            # If close enough to target, stop
            if distance < self.character.speed:
                self.target_pos = None
            else:
                # Normalize direction and apply speed
                dx = (dist_x / distance) * self.character.speed
                dy = (dist_y / distance) * self.character.speed

        self.character.move(dx, dy, self.screen.get_width(), self.screen.get_height())

        # Update target marker timer
        if self.target_marker_timer > 0:
            self.target_marker_timer -= 1

    def draw(self):
        """Draw the game screen."""
        # Draw background (grass-like)
        self.screen.fill((34, 139, 34))

        # Draw simple "grass" pattern
        for x in range(0, self.screen.get_width(), 40):
            for y in range(0, self.screen.get_height(), 40):
                pygame.draw.rect(self.screen, (40, 150, 40), (x + 5, y + 5, 10, 10))

        # Draw target marker if active
        if self.target_marker_timer > 0 and self.target_pos:
            # Pulsing circle effect
            pulse = (self.target_marker_timer % 20) / 20.0
            radius = int(8 + pulse * 4)
            alpha = int(255 * (self.target_marker_timer / 60.0))

            # Create a surface for the marker with alpha
            marker_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
            color_with_alpha = (255, 255, 100, alpha)
            pygame.draw.circle(marker_surface, color_with_alpha, (radius + 2, radius + 2), radius, 2)

            # Draw X in the center
            pygame.draw.line(marker_surface, color_with_alpha,
                           (radius - 3, radius - 3), (radius + 7, radius + 7), 2)
            pygame.draw.line(marker_surface, color_with_alpha,
                           (radius + 7, radius - 3), (radius - 3, radius + 7), 2)

            self.screen.blit(marker_surface,
                           (self.target_pos[0] - radius - 2, self.target_pos[1] - radius - 2))

        # Draw character
        self.screen.blit(self.sprite, (self.character.x, self.character.y))

        # Draw HUD
        char_info = self.font.render(
            f"Character: {self.character.name} | WASD/Arrows or CLICK to move | B: Back | ESC: Quit",
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
