# WASM Deployment Guide

This guide provides detailed instructions for deploying your Zelda-style Python game to the web using WebAssembly (WASM).

## Overview

The game has been converted to be compatible with pygbag, which packages pygame games to run in web browsers using WebAssembly and Pyodide. The game works identically on both desktop and in browsers.

## Changes Made for WASM Compatibility

1. **Async Main Loop**: The `main()` function is now `async def main()` and uses `asyncio.run(main())`
2. **Async Sleep Calls**: Added `await asyncio.sleep(0)` in both game loops to yield control to the browser
3. **PEP 723 Metadata**: Added dependency metadata at the top of main.py for pygbag
4. **Removed sys.exit()**: Replaced with `return` statements for clean shutdown
5. **pygame.quit() Handling**: Properly placed to work in both desktop and browser environments

## Quick Start

### Install Dependencies

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Build for Web

**Linux/Mac:**
```bash
./build_wasm.sh
```

**Windows:**
```bash
build_wasm.bat
```

**Manual:**
```bash
pygbag --build .
```

### Test Locally

```bash
pygbag --server .
```

Then open http://localhost:8000 in your browser.

## Deployment Options

### 1. GitHub Pages (Recommended for Free Hosting)

#### Method A: Using gh-pages Branch

1. Build the WASM version:
   ```bash
   pygbag --build .
   ```

2. Create and switch to gh-pages branch:
   ```bash
   git checkout -b gh-pages
   ```

3. Copy build files to root:
   ```bash
   cp -r build/web/* .
   git add index.html python-game.apk favicon.png
   ```

4. Commit and push:
   ```bash
   git commit -m "Deploy WASM version to GitHub Pages"
   git push origin gh-pages
   ```

5. Enable GitHub Pages:
   - Go to your repository settings
   - Navigate to "Pages" section
   - Set source to "gh-pages" branch
   - Save

6. Your game will be available at: `https://<username>.github.io/<repository>/`

#### Method B: Using GitHub Actions (Automated)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install pygbag
        run: pip install pygbag

      - name: Build with pygbag
        run: pygbag --build .

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/web
```

### 2. itch.io (Game Distribution Platform)

1. Build the WASM version:
   ```bash
   pygbag --build .
   ```

2. Create a ZIP file:
   ```bash
   cd build/web
   zip -r ../../python-game-web.zip .
   cd ../..
   ```

3. Upload to itch.io:
   - Visit https://itch.io/game/new
   - Fill in your game details
   - Set "Kind of project" to **HTML**
   - Upload `python-game-web.zip`
   - Check **"This file will be played in the browser"**
   - Set viewport dimensions to **800 x 600** (or larger)
   - Configure other settings as desired
   - Click "Save & View Page"

4. Your game is now live on itch.io!

### 3. Custom Web Server

1. Build the WASM version:
   ```bash
   pygbag --build .
   ```

2. Upload the contents of `build/web/` to your web server:
   - `index.html` - The main HTML file
   - `python-game.apk` - The packaged game files
   - `favicon.png` - The icon

3. Configure your web server:
   - Ensure it serves `.apk` files with correct MIME type
   - Enable CORS headers if necessary
   - Use HTTPS for best compatibility

4. Access your game at: `https://yourdomain.com/path/to/index.html`

### 4. Netlify or Vercel

1. Build the WASM version:
   ```bash
   pygbag --build .
   ```

2. Create a `netlify.toml` (for Netlify):
   ```toml
   [build]
     publish = "build/web"
     command = "pip install pygbag && pygbag --build ."
   ```

3. Deploy:
   - Connect your repository to Netlify/Vercel
   - Set the publish directory to `build/web`
   - Deploy!

## Testing Your Deployment

### Browser Compatibility

Test in multiple browsers:
- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari (May have some limitations)
- ✅ Edge

### Performance Testing

- Check FPS in browser console
- Test on different devices (desktop, mobile, tablet)
- Verify all controls work
- Test character selection and movement

### Common Issues

1. **Black screen on load**
   - Check browser console for errors
   - Ensure all files are properly hosted
   - Verify CORS headers if using custom server

2. **Slow loading**
   - First load downloads Python and pygame (may take 10-30 seconds)
   - Subsequent loads are faster due to caching

3. **Controls not working**
   - Click on the game canvas to focus it
   - Check browser compatibility

## Build Customization

### Custom Icon

Replace `favicon.png` in the build output with your custom icon (96x96 recommended).

### Custom Template

Use a custom HTML template:
```bash
pygbag --template mytemplate.html .
```

### App Name and Package

Create `pygbag.json` in your project root:
```json
{
  "app_name": "Zelda Adventure",
  "package": "com.yourdomain.zelda",
  "icon": "custom_icon.png"
}
```

## Performance Optimization

1. **Remove Debug Statements**: Ensure no `print()` calls in production (already done)
2. **Optimize Assets**: Use smaller sprites/images if needed
3. **Reduce FPS**: Lower FPS in browser if needed (edit main.py)
4. **Cache Assets**: Pygbag automatically handles caching

## Continuous Deployment

For automated deployments on every commit:

1. Use GitHub Actions (see Method B above)
2. Configure webhooks to trigger builds
3. Automate testing before deployment

## Monitoring

Track your deployed game:
- Use browser analytics (Google Analytics, etc.)
- Monitor error reports
- Collect user feedback

## Additional Resources

- [Pygbag Documentation](https://pygame-web.github.io/wiki/pygbag/)
- [Pygame Web Wiki](https://pygame-web.github.io/)
- [GitHub Pages Documentation](https://docs.github.com/pages)
- [itch.io HTML5 Games Guide](https://itch.io/docs/creators/html5)

## Support

If you encounter issues:
1. Check the browser console for errors
2. Verify all build files are present
3. Test locally with `pygbag --server .` first
4. Check pygbag documentation for updates
5. Open an issue on GitHub

## License

The game deployment configuration is part of the main project under MIT License.
