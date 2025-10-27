"""
Character definitions and sprite management for the game.
"""
import pygame

class Character:
    """Represents a playable character in the game."""

    def __init__(self, name, color, description, eye_color=None):
        """
        Initialize a character.

        Args:
            name: Character name
            color: Primary color (RGB tuple)
            description: Character description
            eye_color: Optional eye/pupil color (RGB tuple), defaults to black
        """
        self.name = name
        self.color = color
        self.description = description
        self.eye_color = eye_color if eye_color else (0, 0, 0)
        self.x = 400
        self.y = 300
        self.speed = 5
        self.size = 32

    def create_sprite(self):
        """Create a simple pixel art sprite for the character."""
        sprite = pygame.Surface((self.size, self.size))
        sprite.fill(self.color)

        # Add simple pixel art details (eyes, etc.)
        pygame.draw.rect(sprite, (255, 255, 255), (8, 10, 6, 6))  # Left eye
        pygame.draw.rect(sprite, (255, 255, 255), (18, 10, 6, 6))  # Right eye
        pygame.draw.rect(sprite, self.eye_color, (10, 12, 2, 2))  # Left pupil
        pygame.draw.rect(sprite, self.eye_color, (20, 12, 2, 2))  # Right pupil

        return sprite

    def move(self, dx, dy, screen_width, screen_height):
        """
        Move the character by dx, dy pixels.

        Args:
            dx: Change in x position
            dy: Change in y position
            screen_width: Width of the screen (for boundary checking)
            screen_height: Height of the screen (for boundary checking)
        """
        new_x = self.x + dx
        new_y = self.y + dy

        # Keep character within screen boundaries
        if 0 <= new_x <= screen_width - self.size:
            self.x = new_x
        if 0 <= new_y <= screen_height - self.size:
            self.y = new_y


# Define the three playable characters
CHARACTERS = [
    Character("Knight", (50, 100, 200), "A brave warrior with strong defense"),
    Character("Mage", (150, 50, 200), "A powerful spellcaster with magical abilities"),
    Character("Ranger", (50, 200, 100), "A swift archer with high speed"),
]


def get_character_by_index(index):
    """
    Get a character by index.

    Args:
        index: Character index (0-2)

    Returns:
        Character object or None if index is invalid
    """
    if 0 <= index < len(CHARACTERS):
        return CHARACTERS[index]
    return None
