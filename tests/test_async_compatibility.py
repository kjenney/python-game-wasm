"""
Tests for async/WASM compatibility of the game.
"""
import asyncio
import inspect
import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame


class TestAsyncCompatibility:
    """Test cases for async compatibility features."""

    def test_main_is_async_function(self):
        """Test that main() is defined as an async function."""
        from main import main
        assert inspect.iscoroutinefunction(main), "main() should be an async function"

    @pytest.mark.asyncio
    async def test_main_can_run_with_asyncio(self):
        """Test that main() can be executed with asyncio."""
        from main import main

        # Mock pygame to prevent actual window creation
        with patch('main.pygame.init'), \
             patch('main.pygame.display.set_mode') as mock_display, \
             patch('main.pygame.display.set_caption'), \
             patch('main.pygame.time.Clock'), \
             patch('main.pygame.event.get') as mock_events, \
             patch('main.pygame.display.flip'), \
             patch('main.pygame.quit'), \
             patch('main.CharacterSelectionScreen') as mock_selection, \
             patch('main.Game') as mock_game:

            # Setup mocks
            mock_screen = Mock()
            mock_display.return_value = mock_screen

            # Simulate QUIT event on first call to exit the selection loop
            quit_event = Mock()
            quit_event.type = pygame.QUIT
            mock_events.return_value = [quit_event]

            # Run main and verify it completes without error
            try:
                await asyncio.wait_for(main(), timeout=1.0)
            except asyncio.TimeoutError:
                pytest.fail("main() took too long to execute or has infinite loop without await")

    def test_pep_723_metadata_present(self):
        """Test that PEP 723 metadata is present in main.py for pygbag."""
        with open('main.py', 'r') as f:
            content = f.read()

        # Check for PEP 723 script metadata
        assert '# /// script' in content, "PEP 723 metadata block should be present"
        assert '# dependencies = [' in content, "Dependencies section should be present"
        assert 'pygame' in content, "pygame should be listed in dependencies"

    def test_no_sys_exit_in_loops(self):
        """Test that sys.exit() is not called in the main game loops."""
        with open('main.py', 'r') as f:
            lines = f.readlines()

        # Find the async def main() line
        main_start = None
        for i, line in enumerate(lines):
            if 'async def main():' in line:
                main_start = i
                break

        assert main_start is not None, "async def main() should be defined"

        # Check that sys.exit() is not used in the main function
        main_content = ''.join(lines[main_start:])

        # sys.exit should not appear in the main function body
        # (it's only used in event handlers which now use return)
        import re
        sys_exit_calls = re.findall(r'\s+sys\.exit\(\)', main_content)
        assert len(sys_exit_calls) == 0, "sys.exit() should not be called in main function"

    def test_asyncio_sleep_in_loops(self):
        """Test that asyncio.sleep(0) is present in game loops."""
        with open('main.py', 'r') as f:
            content = f.read()

        # Check for asyncio.sleep(0) calls
        assert 'await asyncio.sleep(0)' in content, "await asyncio.sleep(0) should be in game loops"

        # Count occurrences - should have at least 2 (selection loop and game loop)
        count = content.count('await asyncio.sleep(0)')
        assert count >= 2, f"Expected at least 2 await asyncio.sleep(0) calls, found {count}"

    def test_asyncio_run_at_end(self):
        """Test that asyncio.run(main()) is used at the end of the file."""
        with open('main.py', 'r') as f:
            content = f.read()

        assert 'asyncio.run(main())' in content, "asyncio.run(main()) should be at the end"

    def test_pygame_quit_not_followed_by_sys_exit(self):
        """Test that pygame.quit() calls are followed by return, not sys.exit()."""
        with open('main.py', 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if 'pygame.quit()' in line:
                # Check the next few lines for sys.exit()
                # In the async version, quit should be followed by return or end of function
                next_lines = ''.join(lines[i:min(i+5, len(lines))])
                if i < len(lines) - 5:  # Not at the very end
                    # If not the final pygame.quit(), it should be followed by return
                    if 'if event.type == pygame.QUIT:' in ''.join(lines[max(0,i-5):i]):
                        assert 'return' in next_lines, f"pygame.quit() at line {i+1} should be followed by return"


class TestAsyncIntegration:
    """Integration tests for async game loop."""

    @pytest.mark.asyncio
    async def test_character_selection_loop_with_asyncio(self):
        """Test character selection loop works with asyncio."""
        from main import main

        with patch('main.pygame.init'), \
             patch('main.pygame.display.set_mode') as mock_display, \
             patch('main.pygame.display.set_caption'), \
             patch('main.pygame.time.Clock') as mock_clock, \
             patch('main.pygame.event.get') as mock_events, \
             patch('main.pygame.display.flip'), \
             patch('main.pygame.quit'), \
             patch('main.CharacterSelectionScreen') as mock_selection_class, \
             patch('main.Game'):

            # Setup
            mock_screen = Mock()
            mock_display.return_value = mock_screen
            mock_selection = Mock()
            mock_selection_class.return_value = mock_selection

            # First call returns None (no selection), second returns QUIT
            quit_event = Mock()
            quit_event.type = pygame.QUIT
            mock_events.return_value = [quit_event]
            mock_selection.handle_event.return_value = None

            # Should complete without hanging
            try:
                await asyncio.wait_for(main(), timeout=2.0)
                assert True, "Selection loop completed with asyncio"
            except asyncio.TimeoutError:
                pytest.fail("Character selection loop did not yield control to asyncio")

    @pytest.mark.asyncio
    async def test_game_loop_with_asyncio(self):
        """Test main game loop works with asyncio."""
        from main import main

        with patch('main.pygame.init'), \
             patch('main.pygame.display.set_mode') as mock_display, \
             patch('main.pygame.display.set_caption'), \
             patch('main.pygame.time.Clock'), \
             patch('main.pygame.event.get') as mock_events, \
             patch('main.pygame.display.flip'), \
             patch('main.pygame.quit'), \
             patch('main.pygame.key.get_pressed') as mock_keys, \
             patch('main.CharacterSelectionScreen') as mock_selection_class, \
             patch('main.Game') as mock_game_class:

            # Setup mocks
            mock_screen = Mock()
            mock_display.return_value = mock_screen
            mock_selection = Mock()
            mock_selection_class.return_value = mock_selection
            mock_game = Mock()
            mock_game_class.return_value = mock_game

            # Sequence: character selected on first try, then game quits
            select_event = Mock()
            select_event.type = pygame.KEYDOWN
            quit_event = Mock()
            quit_event.type = pygame.QUIT

            call_count = [0]
            def event_side_effect():
                call_count[0] += 1
                if call_count[0] == 1:
                    return [select_event]  # Selection screen
                else:
                    return [quit_event]  # Game screen

            mock_events.side_effect = event_side_effect
            mock_selection.handle_event.return_value = 0  # Select first character
            mock_game.is_running.return_value = True
            mock_keys.return_value = {}

            # Should complete without hanging
            try:
                await asyncio.wait_for(main(), timeout=2.0)
                assert True, "Game loop completed with asyncio"
            except asyncio.TimeoutError:
                pytest.fail("Game loop did not yield control to asyncio")
