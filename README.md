# Image Pathifier

A simple utility to quickly convert clipboard images to file paths for Claude CLI.

## Purpose

When using Claude CLI, you cannot directly paste images. This tool bridges that gap by:
1. Capturing images from your clipboard
2. Saving them to a local directory
3. Automatically copying the file path to clipboard
4. Allowing you to paste the path in Claude CLI

## Features

- 🖼️ **Manual paste control** - Press Ctrl+V to save clipboard image
- 💾 **Sequential naming** - Images saved as img_0001.png, img_0002.png, etc.
- 📋 **Instant path copy** - Path automatically copied to clipboard after saving
- 🎨 **Thumbnail gallery** - Visual grid of saved images, click to copy path
- ⚙️ **Configurable settings** - Save directory, max images, theme, thumbnail size
- ♻️ **Auto-cleanup** - Oldest images deleted when limit reached

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zilhak/ImagePathifier.git
cd ImagePathifier
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python ImagePathifier.py
```

또는

```bash
py ImagePathifier.py  # Windows
```

## Usage

1. **Start the application** - Run `python ImagePathifier.py`
2. **Copy an image** - Copy any image to your clipboard (screenshot, image from browser, etc.)
3. **Press Ctrl+V in the app** - The image will be saved and path copied to clipboard
4. **Paste in Claude CLI** - Simply paste (Ctrl+V) the path in your Claude CLI conversation
5. **Click thumbnails** - Click any thumbnail to copy its path again

### Keyboard Shortcuts

- `Ctrl+V` - Save clipboard image and copy its path

## Configuration

Click the Settings button (⚙) in the app to configure:

- **Save Directory** - Where to save images (default: `./saved_images`)
- **Max Images** - Maximum number of images to keep (5-50, default: 20)
- **Theme** - Dark or Light mode
- **Thumbnail Size** - Size of thumbnail previews (50-200px, default: 100px)

Settings are saved in `settings.json` and persist between sessions.

## Requirements

- Python 3.7+
- Pillow (PIL)
- customtkinter
- pyperclip

## Project Structure

```
ImagePathifier/
├── src/
│   ├── __init__.py
│   ├── main.py              # Program entry point
│   ├── app.py               # Main application class
│   ├── config.py            # Configuration management
│   ├── image_manager.py     # Image file management
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main window UI
│   │   └── settings_window.py # Settings window UI
│   └── utils/
│       ├── __init__.py
│       └── clipboard.py     # Clipboard utilities
├── ImagePathifier.py        # Main run script
├── run.py                   # Alternative run script
├── requirements.txt         # Dependencies
├── settings.json            # User settings (auto-generated)
└── README.md
```

## Recent Improvements

The project has been refactored from a single monolithic file to a modular structure with:

### Structural Improvements
- ✅ **Modular Architecture** - Separated concerns into distinct modules
- ✅ **Clean Code Organization** - UI, business logic, and utilities are properly separated
- ✅ **Reusable Components** - Each module has a single responsibility

### Error Handling
- ✅ **Robust File Operations** - All file operations have proper exception handling
- ✅ **Clipboard Error Management** - Graceful handling of clipboard failures
- ✅ **Image Load Failures** - Stable handling when images can't be loaded
- ✅ **Config Recovery** - Defaults restored if settings file is corrupted

### Code Quality
- ✅ **Type Hints** - Added throughout for better code clarity
- ✅ **Documentation** - Comprehensive docstrings added
- ✅ **Single Responsibility** - Each class/function has one clear purpose
- ✅ **DRY Principle** - Eliminated code duplication

## License

MIT
