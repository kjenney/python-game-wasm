"""
Character selection screen for the game.
"""
import pygame
from characters import CHARACTERS
from version import __version__

# Special index to indicate custom character creation
CREATE_CUSTOM_INDEX = -1


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
        self.total_options = len(CHARACTERS) + 1  # +1 for custom character option
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.character_rects = []  # Store clickable areas for mouse support

    def handle_event(self, event):
        """
        Handle input events for character selection.

        Args:
            event: Pygame event

        Returns:
            Selected character index if confirmed (0-2 for preset characters,
            CREATE_CUSTOM_INDEX for custom character creator), None otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % self.total_options
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % self.total_options
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Return special index if custom character is selected
                if self.selected_index == len(CHARACTERS):
                    return CREATE_CUSTOM_INDEX
                return self.selected_index

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos

                # Check if click is on any character
                for i, rect in enumerate(self.character_rects):
                    if rect.collidepoint(mouse_pos):
                        # Single click selects, double click (or same click) confirms
                        if self.selected_index == i:
                            # Already selected, confirm selection
                            if i == len(CHARACTERS):
                                return CREATE_CUSTOM_INDEX
                            return i
                        else:
                            # Select this character
                            self.selected_index = i
                        break

        elif event.type == pygame.MOUSEMOTION:
            # Highlight character on hover
            mouse_pos = event.pos
            for i, rect in enumerate(self.character_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    break

        return None

    def draw(self):
        """Draw the character selection screen."""
        self.screen.fill((20, 20, 40))  # Dark blue background

        # Clear clickable areas
        self.character_rects = []

        # Draw title
        title = self.font.render("Select Your Character", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw characters (now 4 options including custom)
        char_width = self.screen.get_width() // 4

        # Draw preset characters
        for i, character in enumerate(CHARACTERS):
            x_pos = char_width * i + char_width // 2
            y_pos = self.screen.get_height() // 2

            # Create and draw character sprite (larger for selection)
            sprite_size = 64
            sprite = pygame.Surface((sprite_size, sprite_size))
            sprite.fill(character.color)

            # Add pixel art details with character eye color
            pygame.draw.rect(sprite, (255, 255, 255), (16, 20, 12, 12))  # Left eye
            pygame.draw.rect(sprite, (255, 255, 255), (36, 20, 12, 12))  # Right eye
            pygame.draw.rect(sprite, character.eye_color, (20, 24, 4, 4))  # Left pupil
            pygame.draw.rect(sprite, character.eye_color, (40, 24, 4, 4))  # Right pupil

            sprite_rect = sprite.get_rect(center=(x_pos, y_pos))

            # Store clickable area (expanded for easier clicking)
            clickable_rect = sprite_rect.inflate(40, 160)  # Expand to include name/desc
            self.character_rects.append(clickable_rect)

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

        # Draw "Create Custom" option as 4th choice
        custom_index = len(CHARACTERS)
        x_pos = char_width * custom_index + char_width // 2
        y_pos = self.screen.get_height() // 2

        # Create custom character placeholder sprite with + symbol
        sprite_size = 64
        custom_sprite = pygame.Surface((sprite_size, sprite_size))
        custom_sprite.fill((100, 100, 100))

        # Draw a + symbol
        plus_thickness = 8
        pygame.draw.rect(custom_sprite, (255, 255, 255),
                        (sprite_size // 2 - plus_thickness // 2, 12, plus_thickness, 40))
        pygame.draw.rect(custom_sprite, (255, 255, 255),
                        (12, sprite_size // 2 - plus_thickness // 2, 40, plus_thickness))

        sprite_rect = custom_sprite.get_rect(center=(x_pos, y_pos))

        # Store clickable area for custom character option
        clickable_rect = sprite_rect.inflate(40, 160)
        self.character_rects.append(clickable_rect)

        # Highlight if selected
        if self.selected_index == custom_index:
            pygame.draw.rect(self.screen, (255, 255, 0),
                           sprite_rect.inflate(20, 20), 5)

        self.screen.blit(custom_sprite, sprite_rect)

        # Draw "Create Custom" text
        name_text = self.font.render("Create", True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(x_pos, y_pos + 60))
        self.screen.blit(name_text, name_rect)

        name_text2 = self.font.render("Custom", True, (255, 255, 255))
        name_rect2 = name_text2.get_rect(center=(x_pos, y_pos + 85))
        self.screen.blit(name_text2, name_rect2)

        desc_text = self.small_font.render("Design your own", True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(x_pos, y_pos + 115))
        self.screen.blit(desc_text, desc_rect)

        # Draw instructions
        instructions = self.small_font.render(
            "LEFT/RIGHT arrows or HOVER to select | ENTER/SPACE or CLICK to confirm",
            True, (180, 180, 180)
        )
        instr_rect = instructions.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )
        self.screen.blit(instructions, instr_rect)

        # Draw version number in bottom left corner
        version_text = self.small_font.render(f"v{__version__}", True, (120, 120, 120))
        self.screen.blit(version_text, (10, self.screen.get_height() - 30))
