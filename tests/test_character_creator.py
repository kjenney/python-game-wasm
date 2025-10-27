"""
Tests for the character creator module.
"""
import unittest
from unittest.mock import Mock, patch
import pygame


class TestCharacterCreator(unittest.TestCase):
    """Test cases for the CharacterCreator class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock pygame to avoid actual initialization
        self.screen_mock = Mock()
        self.screen_mock.get_width.return_value = 800
        self.screen_mock.get_height.return_value = 600

        # Set up pygame mocks
        self.pygame_patches = [
            patch('character_creator.pygame.font.Font'),
            patch('character_creator.pygame.Surface'),
            patch('character_creator.pygame.draw.rect'),
            patch('character_creator.pygame.draw.line'),
            patch('character_creator.pygame.Rect'),
        ]

        # Start all patches
        self.mocks = [p.start() for p in self.pygame_patches]

        # Configure Font mock
        mock_font_instance = Mock()
        mock_font_instance.render = Mock(return_value=Mock(get_width=Mock(return_value=100)))
        self.mocks[0].return_value = mock_font_instance

        # Configure Surface mock to return proper mock instances
        def surface_side_effect(*args, **kwargs):
            mock_surf = Mock()
            mock_surf.fill = Mock()
            mock_surf.get_width = Mock(return_value=100)
            return mock_surf

        self.mocks[1].side_effect = surface_side_effect

    def tearDown(self):
        """Clean up patches."""
        for p in self.pygame_patches:
            p.stop()

    def test_character_creator_initialization(self):
        """Test that CharacterCreator initializes correctly."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)

        # Check initial state
        self.assertEqual(creator.name, "")
        self.assertEqual(creator.body_color, [128, 128, 128])  # Default gray
        self.assertEqual(creator.selected_eye_color_index, 0)
        self.assertTrue(creator.name_input_active)
        self.assertEqual(creator.active_slider, 0)

    def test_name_input_handling(self):
        """Test name input functionality."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)

        # Test adding characters to name
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        event.unicode = 'a'

        result = creator.handle_event(event)
        self.assertEqual(creator.name, "a")
        self.assertIsNone(result)

        # Test adding more characters
        event.unicode = 'b'
        creator.handle_event(event)
        self.assertEqual(creator.name, "ab")

    def test_backspace_handling(self):
        """Test backspace removes characters from name."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "Test"

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_BACKSPACE

        creator.handle_event(event)
        self.assertEqual(creator.name, "Tes")

        creator.handle_event(event)
        self.assertEqual(creator.name, "Te")

    def test_space_handling(self):
        """Test space adds space to name."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "Test"

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        creator.handle_event(event)
        self.assertEqual(creator.name, "Test ")

    def test_name_length_limit(self):
        """Test name is limited to 20 characters."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "12345678901234567890"  # 20 chars

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        event.unicode = 'a'

        creator.handle_event(event)
        self.assertEqual(len(creator.name), 20)  # Should not exceed 20

    def test_tab_switches_modes(self):
        """Test TAB switches between name input and color editing."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        self.assertTrue(creator.name_input_active)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_TAB

        creator.handle_event(event)
        self.assertFalse(creator.name_input_active)

        creator.handle_event(event)
        self.assertTrue(creator.name_input_active)

    def test_color_slider_navigation(self):
        """Test arrow keys navigate color sliders."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name_input_active = False  # Switch to slider mode
        creator.active_slider = 0

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN

        creator.handle_event(event)
        self.assertEqual(creator.active_slider, 1)

        creator.handle_event(event)
        self.assertEqual(creator.active_slider, 2)

        # Should wrap around
        creator.handle_event(event)
        self.assertEqual(creator.active_slider, 0)

        # Test UP key
        event.key = pygame.K_UP
        creator.handle_event(event)
        self.assertEqual(creator.active_slider, 2)

    def test_color_value_adjustment(self):
        """Test left/right arrows adjust color values."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name_input_active = False
        creator.active_slider = 0
        creator.body_color = [128, 128, 128]

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT

        # Increase red value
        creator.handle_event(event)
        self.assertEqual(creator.body_color[0], 133)

        # Decrease red value
        event.key = pygame.K_LEFT
        creator.handle_event(event)
        self.assertEqual(creator.body_color[0], 128)

    def test_color_value_bounds(self):
        """Test color values stay within 0-255 bounds."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name_input_active = False
        creator.active_slider = 0
        creator.body_color = [255, 128, 128]

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT

        # Try to increase beyond 255
        creator.handle_event(event)
        self.assertEqual(creator.body_color[0], 255)

        # Test lower bound
        creator.body_color[0] = 0
        event.key = pygame.K_LEFT
        creator.handle_event(event)
        self.assertEqual(creator.body_color[0], 0)

    def test_preset_selection(self):
        """Test preset color selection with number keys."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name_input_active = False

        # Test Knight preset (1 key)
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_1
        creator.handle_event(event)
        self.assertEqual(creator.body_color, [50, 100, 200])

        # Test Mage preset (2 key)
        event.key = pygame.K_2
        creator.handle_event(event)
        self.assertEqual(creator.body_color, [150, 50, 200])

        # Test Ranger preset (3 key)
        event.key = pygame.K_3
        creator.handle_event(event)
        self.assertEqual(creator.body_color, [50, 200, 100])

        # Test Custom preset (4 key)
        event.key = pygame.K_4
        creator.handle_event(event)
        self.assertEqual(creator.body_color, [128, 128, 128])

    def test_eye_color_cycling(self):
        """Test E key cycles through eye colors."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name_input_active = False
        initial_index = creator.selected_eye_color_index

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_e

        creator.handle_event(event)
        self.assertEqual(creator.selected_eye_color_index, (initial_index + 1) % 6)

        # Cycle through all
        for _ in range(5):
            creator.handle_event(event)

        # Should wrap back to start
        self.assertEqual(creator.selected_eye_color_index, initial_index)

    def test_escape_cancels_creation(self):
        """Test ESC returns False to cancel creation."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = creator.handle_event(event)
        self.assertFalse(result)

    def test_enter_without_name_returns_none(self):
        """Test ENTER without name does not create character."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = ""

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RETURN

        result = creator.handle_event(event)
        self.assertIsNone(result)

    def test_enter_with_name_creates_character(self):
        """Test ENTER with name creates character."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "Hero"
        creator.body_color = [100, 150, 200]
        creator.eye_color = (255, 100, 100)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RETURN

        result = creator.handle_event(event)

        # Should return a Character object
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Hero")
        self.assertEqual(result.color, (100, 150, 200))
        self.assertEqual(result.eye_color, (255, 100, 100))

    def test_create_character_method(self):
        """Test create_character returns Character with correct attributes."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "MyHero"
        creator.body_color = [200, 100, 50]
        creator.eye_color = (100, 255, 100)

        character = creator.create_character()

        self.assertEqual(character.name, "MyHero")
        self.assertEqual(character.color, (200, 100, 50))
        self.assertEqual(character.eye_color, (100, 255, 100))
        self.assertEqual(character.description, "A custom hero created by the player")

    def test_draw_method_renders(self):
        """Test draw method renders without errors."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)
        creator.name = "Test"

        # Should not raise any exceptions
        try:
            creator.draw()
            draw_succeeded = True
        except Exception:
            draw_succeeded = False

        self.assertTrue(draw_succeeded)

    def test_update_preview_called_on_changes(self):
        """Test preview updates when character attributes change."""
        from character_creator import CharacterCreator

        creator = CharacterCreator(self.screen_mock)

        # Change name
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        event.unicode = 'a'
        creator.handle_event(event)

        # Preview should be updated
        creator.update_preview()
        self.assertIsNotNone(creator.preview_sprite)


if __name__ == '__main__':
    unittest.main()
