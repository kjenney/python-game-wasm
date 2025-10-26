"""
Character selection screen for the game.
"""
import pygame
from characters import CHARACTERS


class CharacterSelectionScreen:
    """Handles the character selection interface."""

    def __init__(self, screen):
        """
        Initialize the character selection screen.

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.selected_index = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def handle_event(self, event):
        """
        Handle input events for character selection.

        Args:
            event: Pygame event

        Returns:
            Selected character index if confirmed, None otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(CHARACTERS)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(CHARACTERS)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.selected_index
        return None

    def draw(self):
        """Draw the character selection screen."""
        self.screen.fill((20, 20, 40))  # Dark blue background

        # Draw title
        title = self.font.render("Select Your Character", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw characters
        char_width = self.screen.get_width() // 3
        for i, character in enumerate(CHARACTERS):
            x_pos = char_width * i + char_width // 2
            y_pos = self.screen.get_height() // 2

            # Create and draw character sprite (larger for selection)
            sprite_size = 64
            sprite = pygame.Surface((sprite_size, sprite_size))
            sprite.fill(character.color)

            # Add pixel art details
            pygame.draw.rect(sprite, (255, 255, 255), (16, 20, 12, 12))  # Left eye
            pygame.draw.rect(sprite, (255, 255, 255), (36, 20, 12, 12))  # Right eye
            pygame.draw.rect(sprite, (0, 0, 0), (20, 24, 4, 4))  # Left pupil
            pygame.draw.rect(sprite, (0, 0, 0), (40, 24, 4, 4))  # Right pupil

            sprite_rect = sprite.get_rect(center=(x_pos, y_pos))

            # Highlight selected character
            if i == self.selected_index:
                pygame.draw.rect(self.screen, (255, 255, 0),
                               sprite_rect.inflate(20, 20), 5)

            self.screen.blit(sprite, sprite_rect)

            # Draw character name
            name_text = self.font.render(character.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(x_pos, y_pos + 60))
            self.screen.blit(name_text, name_rect)

            # Draw character description
            desc_words = character.description.split()
            line1 = " ".join(desc_words[:4])
            line2 = " ".join(desc_words[4:])

            desc_text1 = self.small_font.render(line1, True, (200, 200, 200))
            desc_rect1 = desc_text1.get_rect(center=(x_pos, y_pos + 90))
            self.screen.blit(desc_text1, desc_rect1)

            if line2:
                desc_text2 = self.small_font.render(line2, True, (200, 200, 200))
                desc_rect2 = desc_text2.get_rect(center=(x_pos, y_pos + 110))
                self.screen.blit(desc_text2, desc_rect2)

        # Draw instructions
        instructions = self.small_font.render(
            "Use LEFT/RIGHT arrows to select, ENTER/SPACE to confirm",
            True, (180, 180, 180)
        )
        instr_rect = instructions.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )
        self.screen.blit(instructions, instr_rect)
