"""
Tests for character selection functionality.
"""
import pytest
import pygame
import sys
import os
from unittest.mock import Mock, MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character_selection import CharacterSelectionScreen
from characters import CHARACTERS


class TestCharacterSelectionScreen:
    """Test the character selection screen."""

    def test_initialization(self):
        """Test that the selection screen initializes correctly."""
        # Create a mock screen
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        # Mock pygame.font.Font at the module import location
        with patch('character_selection.pygame.font.Font') as mock_font:
            mock_font.return_value = Mock()
            selection = CharacterSelectionScreen(screen)
            assert selection.screen == screen
            assert selection.selected_index == 0
            assert selection.font is not None
            assert selection.small_font is not None

    def test_handle_event_right_key(self):
        """Test handling right arrow key."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_RIGHT
            result = selection.handle_event(event)
            assert result is None
            assert selection.selected_index == 1

    def test_handle_event_left_key(self):
        """Test handling left arrow key."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)
            selection.selected_index = 1

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_LEFT
            result = selection.handle_event(event)
            assert result is None
            assert selection.selected_index == 0

    def test_handle_event_wrap_around(self):
        """Test that selection wraps around."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)

            # Start at 0, press left should wrap to last option (custom character)
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_LEFT
            selection.handle_event(event)
            # Should wrap to last option (total_options - 1, which is 3 for 4 options)
            assert selection.selected_index == selection.total_options - 1

            # Press right to wrap back to 0
            event.key = pygame.K_RIGHT
            selection.handle_event(event)
            assert selection.selected_index == 0

    def test_handle_event_enter_confirms(self):
        """Test that Enter key confirms selection."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)
            selection.selected_index = 1

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_RETURN
            result = selection.handle_event(event)
            assert result == 1

    def test_handle_event_space_confirms(self):
        """Test that Space key confirms selection."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)
            selection.selected_index = 2

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_SPACE
            result = selection.handle_event(event)
            assert result == 2

    def test_handle_event_other_keys(self):
        """Test that other keys don't affect selection."""
        screen = Mock()
        with patch('character_selection.pygame.font.Font'):
            selection = CharacterSelectionScreen(screen)
            initial_index = selection.selected_index

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_a
            result = selection.handle_event(event)
            assert result is None
            assert selection.selected_index == initial_index

    def test_mouse_hover_changes_selection(self):
        """Test that hovering over a character changes selection."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('character_selection.pygame.font.Font'):
            with patch('character_selection.pygame.Surface'):
                with patch('character_selection.pygame.draw.rect'):
                    selection = CharacterSelectionScreen(screen)
                    # Draw to populate character_rects
                    selection.draw()

                    # Manually create proper rects for testing
                    selection.character_rects = [
                        pygame.Rect(0, 200, 200, 224),    # Character 0
                        pygame.Rect(200, 200, 200, 224),  # Character 1
                        pygame.Rect(400, 200, 200, 224),  # Character 2
                        pygame.Rect(600, 200, 200, 224),  # Character 3 (custom)
                    ]

                    # Simulate hover over second character
                    event = Mock()
                    event.type = pygame.MOUSEMOTION
                    event.pos = (300, 300)  # Inside second character rect

                    selection.handle_event(event)
                    assert selection.selected_index == 1

    def test_mouse_click_confirms_selection(self):
        """Test that clicking on an already selected character confirms it."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('character_selection.pygame.font.Font'):
            with patch('character_selection.pygame.Surface'):
                with patch('character_selection.pygame.draw.rect'):
                    selection = CharacterSelectionScreen(screen)
                    selection.selected_index = 0

                    # Manually create proper rects for testing
                    selection.character_rects = [
                        pygame.Rect(0, 200, 200, 224),
                        pygame.Rect(200, 200, 200, 224),
                        pygame.Rect(400, 200, 200, 224),
                        pygame.Rect(600, 200, 200, 224),
                    ]

                    # Simulate click on first character (already selected)
                    event = Mock()
                    event.type = pygame.MOUSEBUTTONDOWN
                    event.button = 1
                    event.pos = (100, 300)  # Inside first character rect

                    result = selection.handle_event(event)
                    assert result == 0

    def test_mouse_click_selects_different_character(self):
        """Test that clicking on a different character selects it."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('character_selection.pygame.font.Font'):
            with patch('character_selection.pygame.Surface'):
                with patch('character_selection.pygame.draw.rect'):
                    selection = CharacterSelectionScreen(screen)
                    selection.selected_index = 0

                    # Manually create proper rects for testing
                    selection.character_rects = [
                        pygame.Rect(0, 200, 200, 224),
                        pygame.Rect(200, 200, 200, 224),
                        pygame.Rect(400, 200, 200, 224),
                        pygame.Rect(600, 200, 200, 224),
                    ]

                    # Simulate click on second character
                    event = Mock()
                    event.type = pygame.MOUSEBUTTONDOWN
                    event.button = 1
                    event.pos = (300, 300)  # Inside second character rect

                    result = selection.handle_event(event)
                    # First click selects, doesn't confirm
                    assert result is None
                    assert selection.selected_index == 1

    def test_mouse_click_outside_does_nothing(self):
        """Test that clicking outside character areas does nothing."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('character_selection.pygame.font.Font'):
            with patch('character_selection.pygame.Surface'):
                with patch('character_selection.pygame.draw.rect'):
                    selection = CharacterSelectionScreen(screen)
                    selection.selected_index = 0

                    # Manually create proper rects for testing
                    selection.character_rects = [
                        pygame.Rect(0, 200, 200, 224),
                        pygame.Rect(200, 200, 200, 224),
                        pygame.Rect(400, 200, 200, 224),
                        pygame.Rect(600, 200, 200, 224),
                    ]

                    event = Mock()
                    event.type = pygame.MOUSEBUTTONDOWN
                    event.button = 1
                    event.pos = (50, 50)  # Top area, outside all character rects

                    result = selection.handle_event(event)
                    assert result is None
                    assert selection.selected_index == 0  # Should remain unchanged
