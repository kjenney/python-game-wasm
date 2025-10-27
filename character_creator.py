"""
Character Creator Module

This module provides a character creator minigame that allows players
to customize their own character with name, colors, and visual features.
"""

import sys
import pygame
from characters import Character

# Import platform for WASM/mobile keyboard support
if sys.platform == "emscripten":
    import platform


class CharacterCreator:
    """
    Character creator screen that allows players to customize their character.

    Features:
    - Custom name input
    - Body color customization via RGB sliders
    - Eye color customization
    - Real-time preview of character sprite
    - Template selection (Knight, Mage, Ranger presets)
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
        self.name = ""
        self.body_color = list(self.PRESETS["Custom"])  # Start with gray
        self.eye_color = self.EYE_COLORS[0][1]  # Start with blue eyes
        self.selected_eye_color_index = 0

        # UI state
        self.active_slider = 0  # 0=Red, 1=Green, 2=Blue
        self.slider_rects = []
        self.preset_rects = []
        self.eye_color_rects = []
        self.name_input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.name_input_rect = None  # Store text box rect for click detection

        # Preview sprite
        self.preview_sprite = None
        self.update_preview()

        # Start text input to trigger mobile keyboard
        pygame.key.start_text_input()

        # Mobile keyboard support for WASM
        self.mobile_input = None
        self._setup_mobile_input()
        # Show keyboard initially since name input is active by default
        self._show_mobile_keyboard()

    def _setup_mobile_input(self):
        """
        Create a hidden HTML input element for mobile keyboard support.
        This is needed because pygame.key.start_text_input() doesn't trigger
        mobile keyboards in WASM/pygbag builds.
        """
        if sys.platform == "emscripten":
            try:
                # Create an invisible input element
                input_elem = platform.window.document.createElement("input")
                input_elem.type = "text"
                input_elem.id = "mobile-keyboard-input"

                # Style it to be invisible but still functional
                input_elem.style.position = "absolute"
                input_elem.style.left = "-9999px"
                input_elem.style.top = "-9999px"
                input_elem.style.width = "1px"
                input_elem.style.height = "1px"
                input_elem.style.opacity = "0"
                input_elem.style.pointerEvents = "none"

                # Add to document
                platform.window.document.body.appendChild(input_elem)
                self.mobile_input = input_elem
            except Exception as e:
                print(f"Failed to create mobile input element: {e}")

    def _show_mobile_keyboard(self):
        """Focus the hidden input element to trigger mobile keyboard."""
        if sys.platform == "emscripten" and self.mobile_input:
            try:
                self.mobile_input.focus()
            except Exception as e:
                print(f"Failed to focus mobile input: {e}")

    def _hide_mobile_keyboard(self):
        """Blur the hidden input element to hide mobile keyboard."""
        if sys.platform == "emscripten" and self.mobile_input:
            try:
                self.mobile_input.blur()
            except Exception as e:
                print(f"Failed to blur mobile input: {e}")

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
            elif event.key == pygame.K_RETURN:
                if self.name.strip():  # Only allow if name is not empty
                    return self.create_character()
                return None

            # TAB - Switch between name input and slider control
            elif event.key == pygame.K_TAB:
                self.name_input_active = not self.name_input_active
                # Toggle text input to show/hide mobile keyboard
                if self.name_input_active:
                    pygame.key.start_text_input()
                    self._show_mobile_keyboard()
                else:
                    pygame.key.stop_text_input()
                    self._hide_mobile_keyboard()
                return None

            # Handle name input
            if self.name_input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_SPACE:
                    if len(self.name) < 20:
                        self.name += " "
                elif len(self.name) < 20:  # Limit name length
                    if event.unicode.isprintable():
                        self.name += event.unicode
                self.update_preview()
                return None

            # Handle slider/color selection when not in name input mode
            if not self.name_input_active:
                if event.key == pygame.K_UP:
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

        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                # Check if click is on name input box
                if self.name_input_rect and self.name_input_rect.collidepoint(mouse_pos):
                    # Activate name input mode if not already active
                    if not self.name_input_active:
                        self.name_input_active = True
                        pygame.key.start_text_input()
                        self._show_mobile_keyboard()
                else:
                    # Clicked outside text box - deactivate name input
                    if self.name_input_active:
                        self.name_input_active = False
                        pygame.key.stop_text_input()
                        self._hide_mobile_keyboard()

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

        # Name input section
        name_y = 230
        name_label = self.small_font.render("Name:", True, (255, 255, 255))
        self.screen.blit(name_label, (50, name_y))

        # Name input box
        name_box_rect = pygame.Rect(50, name_y + 30, 300, 40)
        self.name_input_rect = name_box_rect  # Store for click detection
        box_color = (100, 100, 255) if self.name_input_active else (80, 80, 80)
        pygame.draw.rect(self.screen, box_color, name_box_rect, 2)

        # Set text input rect for mobile keyboard positioning
        if self.name_input_active:
            pygame.key.set_text_input_rect(name_box_rect)

        # Draw name text with cursor
        name_text = self.small_font.render(self.name, True, (255, 255, 255))
        self.screen.blit(name_text, (55, name_y + 38))

        # Blinking cursor
        if self.name_input_active:
            self.cursor_timer += 1
            if self.cursor_timer % 60 < 30:  # Blink every 30 frames
                cursor_x = 55 + name_text.get_width() + 2
                pygame.draw.line(self.screen, (255, 255, 255),
                               (cursor_x, name_y + 35),
                               (cursor_x, name_y + 60), 2)

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
        rgb_label = self.small_font.render("Body Color (Arrow keys):", True, (255, 255, 255))
        self.screen.blit(rgb_label, (slider_x, rgb_slider_y))

        slider_names = ["Red", "Green", "Blue"]
        for i, slider_name in enumerate(slider_names):
            s_y = rgb_slider_y + 30 + i * 40

            # Label
            is_active_slider = (i == self.active_slider and not self.name_input_active)
            label_color = (255, 255, 100) if is_active_slider else (200, 200, 200)
            label = self.small_font.render(f"{slider_name}:", True, label_color)
            self.screen.blit(label, (slider_x, s_y))

            # Slider bar
            slider_rect = pygame.Rect(slider_x + 70, s_y + 5, 200, 20)
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
            "TAB: Switch between name/color editing",
            "ENTER: Create character (name required)",
            "ESC: Cancel and go back"
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

    # Stop text input when exiting
    pygame.key.stop_text_input()

    # Clean up mobile input element
    if sys.platform == "emscripten" and creator.mobile_input:
        try:
            platform.window.document.body.removeChild(creator.mobile_input)
        except Exception as e:
            print(f"Failed to remove mobile input element: {e}")

    return result if result is not False else None
