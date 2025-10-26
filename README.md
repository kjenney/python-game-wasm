# Zelda-Style Python Game

A simple Zelda-style adventure game built with pygame, featuring character selection and pixel-art graphics.

Check it out live at https://kjenney.github.io/python-game-wasm/

## Features

- **3 Playable Characters**: Choose between Knight, Mage, or Ranger
- **Character Selection Screen**: Navigate with arrow keys, confirm with Enter/Space
- **Movement Controls**: Use WASD or Arrow keys to move your character
- **Pixel Art Style**: Simple, retro-inspired graphics
- **Boundary Detection**: Characters stay within screen bounds

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
source venv/bin/activate  # If not already activated
python main.py
```

## Controls

### Character Selection
- **LEFT/RIGHT Arrow**: Navigate between characters
- **ENTER or SPACE**: Confirm selection

### Gameplay
- **Arrow Keys** or **WASD**: Move character
- **ESC**: Quit game

## Characters

1. **Knight** (Blue) - A brave warrior with strong defense
2. **Mage** (Purple) - A powerful spellcaster with magical abilities
3. **Ranger** (Green) - A swift archer with high speed

## Testing

Run tests:
```bash
source venv/bin/activate
pytest tests/ -v
```

**Note**: There is a known compatibility issue between pygame 2.6.1 and Python 3.14 regarding the font module during testing. Core game logic tests (9/26 tests) pass successfully. The game runs correctly when executed directly via `python main.py`.

## Project Structure

```
python-game/
├── main.py                 # Entry point
├── game.py                 # Main game logic
├── character_selection.py  # Character selection screen
├── characters.py           # Character definitions
├── requirements.txt        # Dependencies
├── tests/                  # Test suite
│   ├── test_characters.py
│   ├── test_character_selection.py
│   └── test_game.py
└── README.md
```

## Development

The game follows pygame best practices (2025):
- Organized game loop structure
- Separation of concerns (characters, game logic, UI)
- Comprehensive test coverage
- Mock-based unit testing
- Async-compatible for WASM deployment

## WASM Deployment

The game can be deployed to run in web browsers using WebAssembly (WASM) via pygbag.

### Building for WASM

**Linux/Mac:**
```bash
./build_wasm.sh
```

**Windows:**
```bash
build_wasm.bat
```

**Manual build:**
```bash
pygbag --build .
```

The build output will be in `build/web/`.

### Testing Locally

Run a local test server:
```bash
pygbag .
```

Then open http://localhost:8000 in your browser.

The test server is enabled by default. For debugging, you can access:
- `http://localhost:8000?-i` - Terminal with REPL and sized-down canvas
- `http://localhost:8000/#debug` - Verbose output for troubleshooting

### Deploying to the Web

#### Option 1: GitHub Pages

1. Create a new branch for GitHub Pages:
```bash
git checkout -b gh-pages
```

2. Build the WASM version:
```bash
pygbag --build .
```

3. Copy the build files to the root:
```bash
cp -r build/web/* .
```

4. Commit and push:
```bash
git add index.html python-game.apk favicon.png
git commit -m "Deploy WASM version"
git push origin gh-pages
```

5. Enable GitHub Pages in your repository settings, pointing to the `gh-pages` branch.

#### Option 2: itch.io

1. Build the WASM version:
```bash
pygbag --build .
```

2. Create a ZIP file of the build directory:
```bash
cd build/web
zip -r python-game.zip *
```

3. Upload to itch.io:
   - Go to https://itch.io/game/new
   - Set "Kind of project" to "HTML"
   - Upload the `python-game.zip` file
   - Check "This file will be played in the browser"
   - Set dimensions to 800x600 (or larger)
   - Publish!

### WASM Compatibility Notes

- The game uses async/await for browser compatibility
- `await asyncio.sleep(0)` calls in the game loop allow the browser to process events
- Works on desktop Python and in web browsers
- No code changes needed to run in either environment

## License

MIT License
