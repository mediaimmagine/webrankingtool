#!/bin/bash

echo "========================================"
echo "Building macOS Portable Application"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "Installing required packages..."
pip3 install -r requirements_image_resizer.txt
pip3 install pyinstaller

echo ""
echo "Building application..."
pyinstaller --clean build_macos.spec

echo ""
echo "========================================"
echo "Build complete!"
echo "========================================"
echo ""
echo "Application location: dist/ImageResizerCOED.app"
echo ""
echo "You can now:"
echo "1. Open dist/ImageResizerCOED.app to run the application"
echo "2. Copy ImageResizerCOED.app to your Applications folder"
echo "3. Distribute the .app file to other Mac users"
echo ""

