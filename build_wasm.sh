#!/bin/bash
# Build script for deploying the game to WASM using pygbag

echo "Building Zelda-Style Game for WASM..."
echo "======================================="

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "Error: pygbag is not installed"
    echo "Please install it with: pip install pygbag"
    exit 1
fi

# Clean previous build
if [ -d "build" ]; then
    echo "Cleaning previous build..."
    rm -rf build
fi

# Build with pygbag
echo "Building with pygbag..."
pygbag --template noctx.tmpl .

echo ""
echo "Build complete!"
echo "==============="
echo ""
echo "To test locally, run: pygbag --server ."
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "To deploy to GitHub Pages or itch.io, upload the contents of the 'build/web' directory"
