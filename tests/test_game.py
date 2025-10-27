"""
Tests for game logic.
"""
import pytest
import pygame
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game import Game


class KeySequence:
    """Mock sequence for pygame key states that supports large key indices."""

    def __init__(self):
        self._keys = {}

    def __getitem__(self, key):
        return self._keys.get(key, False)

    def __setitem__(self, key, value):
        self._keys[key] = value


class TestGame:
    """Test the Game class."""

    def test_initialization(self):
        """Test that the game initializes correctly."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)  # Knight
            assert game.screen == screen
            assert game.character is not None
            assert game.character.name == "Knight"
            assert game.sprite is not None
            assert game.running is True

    def test_initialization_different_characters(self):
        """Test initialization with different characters."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game1 = Game(screen, 1)  # Mage
            assert game1.character.name == "Mage"

            game2 = Game(screen, 2)  # Ranger
            assert game2.character.name == "Ranger"

    def test_handle_event_escape(self):
        """Test that ESC key stops the game."""
        screen = Mock()
        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            assert game.running is True

            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_ESCAPE
            game.handle_event(event)
            assert game.running is False

    def test_is_running(self):
        """Test the is_running method."""
        screen = Mock()
        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            assert game.is_running() is True

            game.running = False
            assert game.is_running() is False

    def test_update_movement_up(self):
        """Test that up movement works."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_y = game.character.y

            # Simulate pressing UP key
            keys = KeySequence()
            keys[pygame.K_UP] = True
            game.update(keys)

            assert game.character.y < initial_y

    def test_update_movement_down(self):
        """Test that down movement works."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_y = game.character.y

            # Simulate pressing DOWN key
            keys = KeySequence()
            keys[pygame.K_DOWN] = True
            game.update(keys)

            assert game.character.y > initial_y

    def test_update_movement_left(self):
        """Test that left movement works."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_x = game.character.x

            # Simulate pressing LEFT key
            keys = KeySequence()
            keys[pygame.K_LEFT] = True
            game.update(keys)

            assert game.character.x < initial_x

    def test_update_movement_right(self):
        """Test that right movement works."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_x = game.character.x

            # Simulate pressing RIGHT key
            keys = KeySequence()
            keys[pygame.K_RIGHT] = True
            game.update(keys)

            assert game.character.x > initial_x

    def test_update_movement_wasd(self):
        """Test that WASD keys work for movement."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_x = game.character.x
            initial_y = game.character.y

            # Test W key (up)
            keys = KeySequence()
            keys[pygame.K_w] = True
            game.update(keys)
            assert game.character.y < initial_y

            # Reset position
            game.character.y = initial_y

            # Test A key (left)
            keys = KeySequence()
            keys[pygame.K_a] = True
            game.update(keys)
            assert game.character.x < initial_x

    def test_update_no_movement(self):
        """Test that no keys pressed means no movement."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            initial_x = game.character.x
            initial_y = game.character.y

            keys = KeySequence()
            game.update(keys)

            assert game.character.x == initial_x
            assert game.character.y == initial_y

    def test_mouse_click_sets_target(self):
        """Test that mouse click sets target position."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            # Simulate mouse click
            event = Mock()
            event.type = pygame.MOUSEBUTTONDOWN
            event.button = 1
            event.pos = (500, 300)

            game.handle_event(event)

            assert game.target_pos == (500, 300)
            assert game.target_marker_timer == 60

    def test_click_to_move_moves_character(self):
        """Test that character moves toward clicked position."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            game.character.x = 100
            game.character.y = 100

            # Set target to the right
            game.target_pos = (200, 100)

            keys = KeySequence()
            game.update(keys)

            # Character should have moved toward target
            assert game.character.x > 100

    def test_keyboard_cancels_click_to_move(self):
        """Test that keyboard input cancels click-to-move."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            # Set a target
            game.target_pos = (500, 300)

            # Press a key
            keys = KeySequence()
            keys[pygame.K_UP] = True
            game.update(keys)

            # Target should be cancelled
            assert game.target_pos is None

    def test_character_stops_at_target(self):
        """Test that character stops when reaching target."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)
            game.character.x = 100
            game.character.y = 100
            game.character.speed = 5

            # Set target to character's center (character center is at x + size/2, y + size/2)
            char_center_x = game.character.x + game.character.size // 2
            char_center_y = game.character.y + game.character.size // 2
            game.target_pos = (char_center_x + 2, char_center_y + 2)

            keys = KeySequence()
            game.update(keys)

            # Character should have reached target and stopped (distance < speed)
            assert game.target_pos is None

    def test_target_marker_timer_decrements(self):
        """Test that target marker timer decrements each update."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            game.target_marker_timer = 60

            keys = KeySequence()
            game.update(keys)

            assert game.target_marker_timer == 59

    def test_return_to_selection_flag_defaults_false(self):
        """Test that return_to_selection flag is False by default."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            assert game.return_to_selection is False

    def test_b_key_sets_return_to_selection(self):
        """Test that pressing B sets return_to_selection and stops game."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            # Simulate pressing B key
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_b

            game.handle_event(event)

            assert game.return_to_selection is True
            assert game.running is False

    def test_escape_does_not_set_return_to_selection(self):
        """Test that ESC stops game but doesn't set return_to_selection."""
        screen = Mock()
        screen.get_width = Mock(return_value=800)
        screen.get_height = Mock(return_value=600)

        with patch('game.pygame.font.Font'):
            game = Game(screen, 0)

            # Simulate pressing ESC key
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_ESCAPE

            game.handle_event(event)

            assert game.return_to_selection is False
            assert game.running is False
