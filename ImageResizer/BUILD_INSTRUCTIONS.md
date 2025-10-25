# Building Portable Executables for Image Resizer COED

This guide explains how to create standalone portable executables for Windows and macOS.

## Windows 11 Portable Executable

### Option 1: Automated Build (Recommended)
1. Double-click `build_portable_windows.bat`
2. Wait for the build to complete
3. Find the executable at `dist\ImageResizerCOED.exe`
4. Distribute the entire `dist` folder or just the .exe file

### Option 2: Manual Build
```bash
# Install dependencies
pip install -r requirements_image_resizer.txt
pip install pyinstaller

# Build executable
pyinstaller --clean build_windows.spec
```

### Windows Distribution
- The executable is completely standalone
- No Python installation required
- Includes all dependencies
- Can be run from USB drive or any location
- Size: ~50-70MB (includes Python runtime and all libraries)

---

## macOS Portable Application

### Building on macOS
1. Open Terminal
2. Navigate to the ImageResizer folder:
   ```bash
   cd path/to/ImageResizer
   ```
3. Make the build script executable:
   ```bash
   chmod +x build_portable_macos.sh
   ```
4. Run the build script:
   ```bash
   ./build_portable_macos.sh
   ```
5. Find the application at `dist/ImageResizerCOED.app`

### Manual Build on macOS
```bash
# Install dependencies
pip3 install -r requirements_image_resizer.txt
pip3 install pyinstaller

# Build application
pyinstaller --clean build_macos.spec
```

### macOS Distribution
- The .app bundle is completely standalone
- No Python installation required
- Can be copied to Applications folder
- Can be distributed to other Mac users
- Compatible with macOS 11 Big Sur (2020) and newer
- Supports: Big Sur, Monterey, Ventura, Sonoma, Sequoia
- Size: ~50-70MB

### Important Note for macOS
When distributing to other users:
1. The app is not code-signed (requires Apple Developer account)
2. Users may need to right-click > Open the first time (Gatekeeper)
3. Or use: System Preferences > Security & Privacy > "Open Anyway"

---

## Build Output Structure

### Windows
```
dist/
└── ImageResizerCOED.exe  (standalone executable)
```

### macOS
```
dist/
└── ImageResizerCOED.app/  (application bundle)
    ├── Contents/
    │   ├── MacOS/
    │   ├── Resources/
    │   └── Info.plist
```

---

## Troubleshooting

### Windows Issues
- **Missing DLL errors**: Rebuild with `--clean` flag
- **Antivirus blocking**: Add exception for PyInstaller builds
- **Large file size**: Normal for bundled Python applications

### macOS Issues
- **"App is damaged"**: User needs to right-click > Open first time
- **Permission denied**: Make sure build script is executable (`chmod +x`)
- **Missing libraries**: Install Xcode Command Line Tools

---

## Testing the Portable Versions

### Windows
1. Copy `dist\ImageResizerCOED.exe` to a test location
2. Double-click to run
3. Test all features (upload, resize, metadata, save)

### macOS
1. Copy `dist/ImageResizerCOED.app` to Applications
2. Right-click > Open (first time only)
3. Test all features

---

## Version Information
- Application: Image Resizer COED Web Optimizer
- Version: 1.0.0
- Bundle ID (macOS): com.mediaimmagine.imageresizerCOED
- Creator: mediaimmagine s.r.l.

---

## Requirements for Building

### Windows
- Windows 10/11
- Python 3.8 or higher
- pip package manager

### macOS
- macOS 11 Big Sur (2020) or newer for running the built app
- macOS 11+ recommended for building
- Python 3.8 or higher
- Xcode Command Line Tools (install with: `xcode-select --install`)

