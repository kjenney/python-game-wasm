"""
Character Creator Module

This module provides a character creator minigame that allows players
to customize their own character with colors and visual features.
"""

import pygame
import random
from characters import Character


class CharacterCreator:
    """
    Character creator screen that allows players to customize their character.

    Features:
    - Body color customization via RGB sliders
    - Eye color customization
    - Real-time preview of character sprite
    - Template selection (Knight, Mage, Ranger presets)
    - Auto-generated random name
    """

    # Color presets based on existing characters
    PRESETS = {
        "Knight": (50, 100, 200),
        "Mage": (150, 50, 200),
        "Ranger": (50, 200, 100),
        "Custom": (128, 128, 128)
    }

    # Eye color options
    EYE_COLORS = [
        ("Blue", (100, 150, 255)),
        ("Green", (100, 255, 150)),
        ("Brown", (139, 69, 19)),
        ("Red", (255, 100, 100)),
        ("Purple", (200, 100, 255)),
        ("Yellow", (255, 255, 100))
    ]

    # Random name parts for character generation
    NAME_PREFIXES = ["Shadow", "Thunder", "Storm", "Fire", "Ice", "Wind", "Star", "Moon", "Sun", "Dragon"]
    NAME_SUFFIXES = ["blade", "walker", "runner", "striker", "dancer", "seeker", "rider", "slayer", "knight", "mage"]

    def __init__(self, screen):
        """
        Initialize the character creator.

        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Character attributes
        # Generate a random name
        self.name = f"{random.choice(self.NAME_PREFIXES)}{random.choice(self.NAME_SUFFIXES)}"
        self.body_color = list(self.PRESETS["Custom"])  # Start with gray
        self.eye_color = self.EYE_COLORS[0][1]  # Start with blue eyes
        self.selected_eye_color_index = 0

        # UI state
        self.active_slider = 0  # 0=Red, 1=Green, 2=Blue
        self.slider_rects = []  # Store slider bar rectangles for mouse interaction
        self.dragging_slider = None  # Track which slider is being dragged (None or 0-2)

        # Preview sprite
        self.preview_sprite = None
        self.update_preview()

        # Back button
        button_width = 100
        button_height = 40
        padding = 10
        self.back_button_rect = pygame.Rect(
            screen.get_width() - button_width - padding,
            padding,
            button_width,
            button_height
        )
        self.back_button_hovered = False

    def update_preview(self):
        """Update the preview sprite with current customization."""
        # Create a temporary character to generate sprite
        temp_char = Character(
            self.name if self.name else "Preview",
            tuple(self.body_color),
            "Custom character"
        )
        # Create larger sprite for preview (128x128)
        size = 128
        sprite = pygame.Surface((size, size))
        sprite.fill((40, 40, 60))  # Dark background

        # Draw character body (80% of size)
        body_size = int(size * 0.8)
        body_rect = pygame.Rect((size - body_size) // 2, (size - body_size) // 2,
                                body_size, body_size)
        pygame.draw.rect(sprite, tuple(self.body_color), body_rect)

        # Draw eyes with selected eye color
        eye_width = body_size // 4
        eye_height = body_size // 6
        eye_y = size // 2 - eye_height // 2

        # Left eye
        left_eye_rect = pygame.Rect(size // 3 - eye_width // 2, eye_y, eye_width, eye_height)
        pygame.draw.rect(sprite, (255, 255, 255), left_eye_rect)
        pupil_size = eye_width // 3
        pygame.draw.rect(sprite, self.eye_color,
                        (left_eye_rect.centerx - pupil_size // 2,
                         left_eye_rect.centery - pupil_size // 2,
                         pupil_size, pupil_size))

        # Right eye
        right_eye_rect = pygame.Rect(2 * size // 3 - eye_width // 2, eye_y, eye_width, eye_height)
        pygame.draw.rect(sprite, (255, 255, 255), right_eye_rect)
        pygame.draw.rect(sprite, self.eye_color,
                        (right_eye_rect.centerx - pupil_size // 2,
                         right_eye_rect.centery - pupil_size // 2,
                         pupil_size, pupil_size))

        self.preview_sprite = sprite

    def handle_event(self, event):
        """
        Handle input events for the character creator.

        Args:
            event: Pygame event object

        Returns:
            Character object if creation is complete, None if still creating,
            False if cancelled
        """
        if event.type == pygame.KEYDOWN:
            # ESC - Cancel and go back
            if event.key == pygame.K_ESCAPE:
                return False

            # ENTER - Confirm character creation
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.create_character()

            # Arrow keys for color adjustment
            elif event.key == pygame.K_UP:
                self.active_slider = (self.active_slider - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.active_slider = (self.active_slider + 1) % 3
            elif event.key == pygame.K_LEFT:
                self.body_color[self.active_slider] = max(0, self.body_color[self.active_slider] - 5)
                self.update_preview()
            elif event.key == pygame.K_RIGHT:
                self.body_color[self.active_slider] = min(255, self.body_color[self.active_slider] + 5)
                self.update_preview()

            # Number keys 1-4 for preset selection
            elif event.key == pygame.K_1:
                self.body_color = list(self.PRESETS["Knight"])
                self.update_preview()
            elif event.key == pygame.K_2:
                self.body_color = list(self.PRESETS["Mage"])
                self.update_preview()
            elif event.key == pygame.K_3:
                self.body_color = list(self.PRESETS["Ranger"])
                self.update_preview()
            elif event.key == pygame.K_4:
                self.body_color = list(self.PRESETS["Custom"])
                self.update_preview()

            # E key to cycle through eye colors
            elif event.key == pygame.K_e:
                self.selected_eye_color_index = (self.selected_eye_color_index + 1) % len(self.EYE_COLORS)
                self.eye_color = self.EYE_COLORS[self.selected_eye_color_index][1]
                self.update_preview()

        # Handle mouse motion for hover detection and dragging
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

            # Check if mouse is hovering over back button
            self.back_button_hovered = self.back_button_rect.collidepoint(mouse_pos)

            # Handle slider dragging
            if self.dragging_slider is not None:
                slider_rect = self.slider_rects[self.dragging_slider]
                # Calculate value based on mouse position within slider
                relative_x = mouse_pos[0] - slider_rect.x
                relative_x = max(0, min(relative_x, slider_rect.width))
                value = int((relative_x / slider_rect.width) * 255)
                self.body_color[self.dragging_slider] = value
                self.active_slider = self.dragging_slider
                self.update_preview()

        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos

                # Check if back button was clicked
                if self.back_button_rect.collidepoint(mouse_pos):
                    return False  # Cancel character creation

                # Check if any slider was clicked
                for i, slider_rect in enumerate(self.slider_rects):
                    if slider_rect.collidepoint(mouse_pos):
                        self.dragging_slider = i
                        self.active_slider = i
                        # Set the value based on click position
                        relative_x = mouse_pos[0] - slider_rect.x
                        relative_x = max(0, min(relative_x, slider_rect.width))
                        value = int((relative_x / slider_rect.width) * 255)
                        self.body_color[i] = value
                        self.update_preview()
                        break

        # Handle mouse button release to stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging_slider = None

        return None

    def create_character(self):
        """
        Create and return a Character object with current customization.

        Returns:
            Character object with custom attributes
        """
        return Character(
            name=self.name if self.name else "Custom Hero",
            color=tuple(self.body_color),
            description="A custom hero created by the player",
            eye_color=self.eye_color
        )

    def draw(self):
        """Draw the character creator interface."""
        # Clear screen with dark background
        self.screen.fill((20, 20, 40))

        # Draw back button (top right)
        button_color = (100, 100, 200) if self.back_button_hovered else (70, 70, 150)
        pygame.draw.rect(self.screen, button_color, self.back_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 255), self.back_button_rect, 2, border_radius=5)

        back_text = self.small_font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)

        # Title
        title = self.font.render("Character Creator", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 20))

        # Draw preview sprite
        preview_x = 50
        preview_y = 80
        if self.preview_sprite:
            self.screen.blit(self.preview_sprite, (preview_x, preview_y))
            # Draw border around preview
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (preview_x - 2, preview_y - 2, 132, 132), 2)

        # Display character name below preview
        name_y = 220
        name_label = self.small_font.render(f"Name: {self.name}", True, (255, 255, 255))
        self.screen.blit(name_label, (50, name_y))

        # Color sliders section
        slider_x = 400
        slider_y = 80

        # Preset buttons
        presets_label = self.small_font.render("Presets (1-4):", True, (255, 255, 255))
        self.screen.blit(presets_label, (slider_x, slider_y))

        preset_names = ["Knight", "Mage", "Ranger", "Custom"]
        for i, preset_name in enumerate(preset_names):
            btn_y = slider_y + 30 + i * 35
            btn_rect = pygame.Rect(slider_x, btn_y, 150, 30)

            # Highlight if current color matches preset
            is_active = list(self.PRESETS[preset_name]) == self.body_color
            btn_color = (100, 150, 255) if is_active else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, btn_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), btn_rect, 2)

            # Draw preset color sample
            color_sample_rect = pygame.Rect(slider_x + 5, btn_y + 5, 20, 20)
            pygame.draw.rect(self.screen, self.PRESETS[preset_name], color_sample_rect)

            # Draw preset name
            preset_text = self.small_font.render(f"{i+1}. {preset_name}", True, (255, 255, 255))
            self.screen.blit(preset_text, (slider_x + 30, btn_y + 5))

        # RGB Sliders
        rgb_slider_y = slider_y + 180
        rgb_label = self.small_font.render("Body Color (Click/drag or arrow keys):", True, (255, 255, 255))
        self.screen.blit(rgb_label, (slider_x, rgb_slider_y))

        # Clear and rebuild slider rects for mouse interaction
        self.slider_rects = []

        slider_names = ["Red", "Green", "Blue"]
        for i, slider_name in enumerate(slider_names):
            s_y = rgb_slider_y + 30 + i * 40

            # Label
            is_active_slider = (i == self.active_slider)
            label_color = (255, 255, 100) if is_active_slider else (200, 200, 200)
            label = self.small_font.render(f"{slider_name}:", True, label_color)
            self.screen.blit(label, (slider_x, s_y))

            # Slider bar
            slider_rect = pygame.Rect(slider_x + 70, s_y + 5, 200, 20)
            self.slider_rects.append(slider_rect)  # Store for mouse interaction
            pygame.draw.rect(self.screen, (60, 60, 80), slider_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), slider_rect, 2)

            # Slider fill
            fill_width = int((self.body_color[i] / 255) * 200)
            fill_rect = pygame.Rect(slider_x + 70, s_y + 5, fill_width, 20)
            slider_color = [0, 0, 0]
            slider_color[i] = 255
            pygame.draw.rect(self.screen, tuple(slider_color), fill_rect)

            # Value text
            value_text = self.small_font.render(str(self.body_color[i]), True, (255, 255, 255))
            self.screen.blit(value_text, (slider_x + 280, s_y))

        # Eye color section
        eye_y = rgb_slider_y + 150
        eye_label = self.small_font.render("Eye Color (E to cycle):", True, (255, 255, 255))
        self.screen.blit(eye_label, (slider_x, eye_y))

        # Current eye color display
        current_eye_name = self.EYE_COLORS[self.selected_eye_color_index][0]
        eye_color_rect = pygame.Rect(slider_x, eye_y + 30, 40, 40)
        pygame.draw.rect(self.screen, self.eye_color, eye_color_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), eye_color_rect, 2)

        eye_name_text = self.small_font.render(current_eye_name, True, (255, 255, 255))
        self.screen.blit(eye_name_text, (slider_x + 50, eye_y + 40))

        # Instructions at bottom
        instructions = [
            "Click/drag sliders or use arrow keys | 1-4: Presets | E: Eye color",
            "ENTER/SPACE or click: Create character",
            "ESC or Back button: Cancel"
        ]

        inst_y = self.screen.get_height() - 80
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (180, 180, 180))
            self.screen.blit(inst_text, (50, inst_y + i * 25))


async def run_character_creator(screen):
    """
    Run the character creator screen.

    Args:
        screen: Pygame display surface

    Returns:
        Character object if created successfully,
        None if cancelled
    """
    import asyncio

    print("=== Entering character creator ===")
    creator = CharacterCreator(screen)
    clock = pygame.time.Clock()

    running = True
    result = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            result = creator.handle_event(event)
            if result is not None:  # Character created or cancelled
                running = False
                break

        if running:
            creator.draw()
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)  # Allow other async tasks to run

    return result if result is not False else None
