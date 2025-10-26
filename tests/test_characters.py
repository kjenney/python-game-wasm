"""
Tests for character functionality.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from characters import Character, CHARACTERS, get_character_by_index


class TestCharacter:
    """Test the Character class."""

    def test_character_initialization(self):
        """Test that a character initializes correctly."""
        char = Character("TestChar", (255, 0, 0), "Test description")
        assert char.name == "TestChar"
        assert char.color == (255, 0, 0)
        assert char.description == "Test description"
        assert char.x == 400
        assert char.y == 300
        assert char.speed == 5
        assert char.size == 32

    def test_character_move_within_bounds(self):
        """Test that character moves correctly within bounds."""
        char = Character("TestChar", (255, 0, 0), "Test")
        original_x = char.x
        original_y = char.y

        char.move(10, 0, 800, 600)
        assert char.x == original_x + 10
        assert char.y == original_y

        char.move(0, 15, 800, 600)
        assert char.x == original_x + 10
        assert char.y == original_y + 15

    def test_character_move_boundary_x(self):
        """Test that character respects x boundaries."""
        char = Character("TestChar", (255, 0, 0), "Test")
        char.x = 0

        # Try to move beyond left boundary
        char.move(-10, 0, 800, 600)
        assert char.x == 0

        # Move to right boundary
        char.x = 768  # 800 - 32 (size)
        char.move(10, 0, 800, 600)
        assert char.x == 768

    def test_character_move_boundary_y(self):
        """Test that character respects y boundaries."""
        char = Character("TestChar", (255, 0, 0), "Test")
        char.y = 0

        # Try to move beyond top boundary
        char.move(0, -10, 800, 600)
        assert char.y == 0

        # Move to bottom boundary
        char.y = 568  # 600 - 32 (size)
        char.move(0, 10, 800, 600)
        assert char.y == 568


class TestCharacterData:
    """Test the predefined character data."""

    def test_characters_count(self):
        """Test that there are exactly 3 characters."""
        assert len(CHARACTERS) == 3

    def test_characters_have_required_attributes(self):
        """Test that all characters have required attributes."""
        for char in CHARACTERS:
            assert hasattr(char, 'name')
            assert hasattr(char, 'color')
            assert hasattr(char, 'description')
            assert isinstance(char.name, str)
            assert isinstance(char.color, tuple)
            assert len(char.color) == 3
            assert isinstance(char.description, str)

    def test_character_names(self):
        """Test that characters have expected names."""
        names = [char.name for char in CHARACTERS]
        assert "Knight" in names
        assert "Mage" in names
        assert "Ranger" in names

    def test_get_character_by_valid_index(self):
        """Test getting characters by valid index."""
        char0 = get_character_by_index(0)
        assert char0 is not None
        assert char0.name == "Knight"

        char1 = get_character_by_index(1)
        assert char1 is not None
        assert char1.name == "Mage"

        char2 = get_character_by_index(2)
        assert char2 is not None
        assert char2.name == "Ranger"

    def test_get_character_by_invalid_index(self):
        """Test getting characters by invalid index."""
        assert get_character_by_index(-1) is None
        assert get_character_by_index(3) is None
        assert get_character_by_index(100) is None
