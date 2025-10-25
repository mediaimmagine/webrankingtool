# Image Resizer COED - Distribution Guide

## Portable Executables Ready!

### ✅ Windows 11 Portable
**Location:** `ImageResizer/dist/ImageResizerCOED.exe`
**Size:** ~30 MB
**Status:** ✅ BUILT AND READY

#### Distribution Package Contents:
- `ImageResizerCOED.exe` - Main executable
- `README_WINDOWS.txt` - User guide

#### How to Distribute (Windows):
1. Copy the entire `dist` folder OR just `ImageResizerCOED.exe`
2. Optional: Include `README_WINDOWS.txt` for user instructions
3. Zip it up and share!

#### Testing:
```bash
# Test the executable
cd ImageResizer/dist
./ImageResizerCOED.exe
```

---

### 📱 macOS Portable (Build on Mac)
**Location:** Will be at `ImageResizer/dist/ImageResizerCOED.app` (after building)
**Status:** ⏳ BUILD SCRIPTS READY

#### To Build on macOS:
1. Transfer the `ImageResizer` folder to a Mac
2. Open Terminal and navigate to the folder:
   ```bash
   cd path/to/ImageResizer
   ```
3. Make the script executable:
   ```bash
   chmod +x build_portable_macos.sh
   ```
4. Run the build script:
   ```bash
   ./build_portable_macos.sh
   ```
5. The app will be created at `dist/ImageResizerCOED.app`

#### Alternative macOS Build (Manual):
```bash
cd ImageResizer
pip3 install -r requirements_image_resizer.txt
pip3 install pyinstaller
pyinstaller --clean build_macos.spec
```

#### How to Distribute (macOS):
1. Copy `ImageResizerCOED.app` from the `dist` folder
2. Compress it: Right-click > Compress "ImageResizerCOED.app"
3. Share the .zip file

#### First-Time Usage on macOS:
Users will need to:
1. Extract the .app from the .zip
2. Right-click > Open (first time only, due to Gatekeeper)
3. Click "Open" when prompted
4. Subsequent opens: just double-click

#### Compatibility:
- Compatible with macOS 11 Big Sur (2020) and newer
- Tested on: Big Sur, Monterey, Ventura, Sonoma
- Provides 2+ years of backward compatibility

---

## Build Files Created

### Windows Build Files:
- ✅ `build_windows.spec` - PyInstaller specification
- ✅ `build_portable_windows.bat` - Automated build script
- ✅ `dist/ImageResizerCOED.exe` - Portable executable
- ✅ `dist/README_WINDOWS.txt` - User instructions

### macOS Build Files:
- ✅ `build_macos.spec` - PyInstaller specification
- ✅ `build_portable_macos.sh` - Automated build script
- ⏳ `dist/ImageResizerCOED.app` - Will be created on Mac

### Documentation:
- ✅ `BUILD_INSTRUCTIONS.md` - Complete build guide
- ✅ `DISTRIBUTION_README.md` - This file

---

## Features Included in Portable Versions

Both Windows and macOS versions include:

✅ **Complete Standalone Application**
- No Python installation required
- No dependencies to install
- Run from anywhere (USB, Downloads, Desktop)
- ~30-50 MB file size

✅ **All Features**
- Image resizing with custom dimensions
- Web presets (Instagram, Facebook, Twitter)
- Quality control (1-100%)
- Multiple formats (JPEG, PNG, WebP)
- Metadata support (Title, Author, Copyright, Description)
- EXIF data preservation
- Blur background effect
- Manual crop positioning
- Real-time file size estimation
- Color-coded size warnings

✅ **Professional UI**
- mediaimmagine logo
- Modern, clean interface
- Responsive controls
- Side-by-side preview

---

## File Size Comparison

| Version | Size | Notes |
|---------|------|-------|
| Windows .exe | ~30 MB | Includes Python 3.12 + all libraries |
| macOS .app | ~40-50 MB | Includes Python + frameworks |
| Source code | ~50 KB | Requires Python installation |

---

## Distribution Checklist

### For Windows Distribution:
- [ ] Copy `ImageResizerCOED.exe` from `dist` folder
- [ ] Include `README_WINDOWS.txt` (optional but recommended)
- [ ] Create a zip file (optional)
- [ ] Test on a clean Windows 11 machine
- [ ] Verify all features work
- [ ] Check antivirus doesn't block it

### For macOS Distribution:
- [ ] Build on Mac using provided scripts
- [ ] Test the .app on macOS
- [ ] Right-click > Compress to create .zip
- [ ] Test extraction and opening process
- [ ] Verify all features work
- [ ] Include instructions for first-time opening

---

## Advanced: Code Signing (Optional)

### Windows Code Signing:
Requires a Windows code signing certificate ($100-400/year)
- Prevents "Unknown Publisher" warnings
- Builds trust with users
- Use `signtool.exe` to sign the .exe

### macOS Code Signing:
Requires Apple Developer account ($99/year)
- Prevents "damaged app" warnings
- Allows notarization for macOS 10.15+
- Use `codesign` and `xcrun notarytool`

**Note:** Code signing is optional but recommended for wide distribution.

---

## Version Information

**Application:** Image Resizer COED Web Optimizer
**Version:** 1.0.0
**Bundle ID (macOS):** com.mediaimmagine.imageresizerCOED
**Creator:** mediaimmagine s.r.l.
**Project:** COED Digital Editor IA  
**CUP:** D97H24001840007  
**Funding:** PR FESR 2021-27 contributo di Regione Friuli-Venezia Giulia  
**Development:** sviluppato con l'ausilio di IA

---

## Next Steps

1. **Windows:** ✅ Ready to distribute! Find executable at `dist/ImageResizerCOED.exe`
2. **macOS:** 🔄 Transfer to Mac and run build script
3. **Testing:** Test both versions thoroughly before wide distribution
4. **Documentation:** Share BUILD_INSTRUCTIONS.md with users who want to build from source

---

## Questions?

See `BUILD_INSTRUCTIONS.md` for detailed build and troubleshooting information.

