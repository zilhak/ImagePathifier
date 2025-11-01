# Image Pathifier

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-green.svg)](README_KR.md)

Convert clipboard images to file paths instantly. Built with Rust for speed and reliability.

## Features

- 🚀 **Fast Startup**: Single executable, no dependencies
- 💾 **Small Size**: ~10MB binary
- ⚡ **Instant Response**: Native Rust performance
- 🎨 **Modern UI**: Clean egui-based interface
- 🔄 **Cross-Platform**: Windows, macOS, Linux
- ⌨️ **Keyboard Shortcuts**: Ctrl+V (Windows/Linux), Cmd+V (macOS)
- 🌏 **Korean Support**: Built-in Korean font support

## Installation

### Option 1: Download Release (Recommended)

Download the latest release for your platform from the [Releases](https://github.com/zilhak/ImagePathifier/releases) page.

### Option 2: Build from Source

**1. Install Rust**

Windows:
```powershell
winget install Rustlang.Rust.GNU
```

macOS/Linux:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**2. Clone and Build**

```bash
git clone https://github.com/zilhak/ImagePathifier.git
cd ImagePathifier

# Build release version
cargo build --release

# Run
./target/release/image-pathifier      # macOS/Linux
.\target\release\image-pathifier.exe  # Windows
```

Or use the build scripts:

```bash
./build.sh       # macOS/Linux
build.bat        # Windows
```

## Usage

1. **Copy an image** to clipboard (screenshot, file copy, etc.)
2. **Press Ctrl+V** (or Cmd+V on macOS) in the app or click the paste button
3. **File path is automatically copied** to your clipboard
4. **Paste the path** into CLI tools like Claude Code

Click on thumbnails to copy their paths again.

## Configuration

Click the ⚙ Settings button to configure:
- **Save Directory**: Where images are stored
- **Max Images**: How many images to keep (1-100)
- **Thumbnail Size**: Display size (50-200px)
- **Theme**: System/Light/Dark mode

Settings are automatically saved.

## Add to Startup (Optional)

### Windows

The build script (`build.bat`) will prompt you to add to startup automatically.

Or manually:
1. Press `Win+R`, type `shell:startup`
2. Create a shortcut to `image-pathifier.exe`

### macOS

Create a LaunchAgent:

```bash
# Create ~/Library/LaunchAgents/com.imagepathifier.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.imagepathifier</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/image-pathifier</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Linux

Create autostart entry:

```bash
# Create ~/.config/autostart/image-pathifier.desktop
[Desktop Entry]
Type=Application
Name=Image Pathifier
Exec=/path/to/image-pathifier
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## Tech Stack

- **GUI**: [egui](https://github.com/emilk/egui) - Immediate mode GUI
- **Clipboard**: [arboard](https://github.com/1Password/arboard) - Cross-platform clipboard
- **Image**: [image](https://github.com/image-rs/image) - Image processing
- **Config**: [confy](https://github.com/rust-cli/confy) - Configuration management

## License

MIT
