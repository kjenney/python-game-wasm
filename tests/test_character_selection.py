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

            # Start at 0, press left should wrap to last character
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_LEFT
            selection.handle_event(event)
            assert selection.selected_index == len(CHARACTERS) - 1

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
