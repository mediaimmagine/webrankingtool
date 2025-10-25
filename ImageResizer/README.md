# 🖼️ Image Resizer & Web Optimizer

A professional, cross-platform image resizing and optimization tool with advanced features including smart cropping, multiple output formats, and copyright detection.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen)
![License](https://img.shields.io/badge/license-Free-green)

## ✨ Features

### 🎯 Smart Resizing
- **Maintain aspect ratio** or set custom dimensions
- **6 web-optimized presets**: 2K, Full HD, HD, Web, Instagram, Thumbnail
- **Real-time preview** with dimensions and file size estimation

### ✂️ Advanced Cropping
- **Auto Center Crop**: Automatically crops to target aspect ratio
- **Manual Positioning**: Interactive drag-and-drop crop positioning
- **Visual Preview**: See exactly what will be cropped before saving
- **Aspect Ratio Lock**: Prevents image distortion

### 💾 Multiple Output Formats
- **JPG/JPEG**: Best for photos, adjustable quality compression (1-100%)
- **PNG**: Lossless compression, transparency support
- **WebP**: Modern format with smallest file sizes

### 🎚️ Quality Control
- **Quick Presets**: 30% (Small), 50% (Medium), 85% (High)
- **Custom Slider**: Fine-tune from 1-100%
- **Real-Time Updates**: File size estimation updates as you adjust

### ⚠️ Copyright Protection
- **Automatic Detection**: Scans EXIF and metadata for copyright information
- **RED WARNING**: Prominent alert for protected images
- **Legal Compliance**: Helps avoid copyright violations

### 🏷️ Professional Output
- **Auto-Prefix**: Files saved as `trieste@news_FILENAME.ext`
- **Optimized Compression**: Format-specific optimization
- **Web-Ready**: Optimized for fast web loading

## 🚀 Quick Start

### Installation

#### Windows
1. Download or clone this repository
2. Double-click `run_image_resizer.bat`
3. Dependencies install automatically!

#### Mac/Linux
```bash
# Clone repository
git clone git@github.com:mediaimmagine/imageresizer.git
cd imageresizer

# Make launcher executable
chmod +x run_image_resizer.sh

# Run
./run_image_resizer.sh
```

#### Manual Installation
```bash
# Install Python 3.7 or higher
# Then install dependencies
pip install -r requirements_image_resizer.txt

# Run directly
python image_resizer.py
```

## 📖 Usage

### Basic Workflow

1. **Upload Image**: Click "📁 Upload Image" and select your image
2. **Choose Preset**: Select from 6 web-optimized presets or enter custom dimensions
3. **Select Format**: Choose JPG, PNG, or WebP for output
4. **Adjust Quality**: Use presets (30%, 50%, 85%) or custom slider
5. **Save**: Click "💾 Save Resized Image"

### Advanced Features

#### Smart Cropping
When selecting a preset with different aspect ratio:
- Crop mode enables automatically
- Check "Manual crop positioning" to adjust crop area
- Drag the orange box to reposition the crop
- Preview updates in real-time

#### Format Selection
- **JPG**: Best for photos, smallest file size
- **PNG**: Best for graphics, logos, transparency
- **WebP**: Modern format, great compression, supported by most browsers

#### Copyright Detection
- Red warning appears if image contains copyright metadata
- Check warning before using/publishing images
- Helps maintain legal compliance

## 📐 Web Presets

| Preset | Dimensions | Aspect Ratio | Best For |
|--------|-----------|--------------|----------|
| **2K** | 2048x1366 | 1.5:1 | High-res web, hero images |
| **Full HD** | 1920x1080 | 16:9 | Standard HD, banners |
| **HD** | 1280x720 | 16:9 | Featured images |
| **Web** | 1024x683 | 1.5:1 | Optimized web content |
| **Instagram** | 1080x1080 | 1:1 | Social media square |
| **Thumbnail** | 400x300 | 4:3 | Small previews |

## 📊 Performance Tips

### File Size Goals
- **Above the fold images**: < 200KB
- **Featured images**: < 150KB
- **Content images**: < 100KB
- **Thumbnails**: < 50KB

### Format Recommendations
- **Photos** → JPG (50-85% quality)
- **Graphics/Logos** → PNG (85%+ quality)
- **Modern web** → WebP (50-80% quality)
- **Maximum compatibility** → JPG

## 🔧 System Requirements

- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.7 or higher
- **Memory**: 256MB RAM minimum
- **Display**: 1200x800 resolution recommended

## 📚 Documentation

- **[Complete User Guide](IMAGE_RESIZER_README.md)** - Detailed documentation
- **[Updates & Changelog](IMAGE_RESIZER_UPDATES.md)** - Version history
- **[Project Summary](IMAGE_RESIZER_PROJECT_SUMMARY.md)** - Technical overview
- **[Crop Feature Guide](CROP_FEATURE_GUIDE.md)** - Cropping instructions
- **[Manual Crop Guide](MANUAL_CROP_GUIDE.md)** - Interactive crop positioning

## 🐛 Troubleshooting

### "No module named 'PIL'"
```bash
pip install Pillow
```

### "tkinter not found"
- **Windows/Mac**: Included with Python
- **Linux**: `sudo apt-get install python3-tk`

### Preview not updating
- Click "🔄 Update Preview" button manually
- Or adjust quality slider (updates automatically)

## 🎨 Customization

### Change Default Quality
Edit line 31 in `image_resizer.py`:
```python
self.quality_var = tk.IntVar(value=50)  # Change 50 to your default
```

### Add Custom Preset
Add to presets list around line 270:
```python
("Custom (800x600)", 800, 600),
```

### Change Auto-Prefix
Edit line 1109 in `image_resizer.py`:
```python
default_name = f"your_prefix_{original_name}{selected_ext}"
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

Free to use for personal and commercial projects.

## 🙏 Credits

**Built with**:
- Python 3.x
- [Pillow (PIL Fork)](https://python-pillow.org/) - Image processing
- Tkinter - GUI framework

**Developed by**: Media Immagine

---

## 📸 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────┐
│        🖼️ Image Resizer & Web Optimizer             │
├─────────────────────┬───────────────────────────────┤
│  CONTROLS (Left)    │  PREVIEW (Right)              │
│                     │                               │
│  📁 Upload Image    │  📸 Live Preview              │
│  ⚙️ Resize Settings  │  📐 Dimensions                │
│  🎚️ Quality Presets │  📊 File Size                 │
│  💾 Output Format   │  ⚠️ Copyright Warning         │
│  🌐 Web Presets     │  🖼️ Image Display             │
│  ✂️ Crop Options    │                               │
│  💾 Save Image      │                               │
└─────────────────────┴───────────────────────────────┘
```

---

## ⭐ Star this repo if you find it useful!

**Issues?** Open an issue on GitHub  
**Questions?** Check the [documentation](IMAGE_RESIZER_README.md)

---

**Version**: 1.0  
**Last Updated**: October 2024  
**Repository**: [github.com/mediaimmagine/imageresizer](https://github.com/mediaimmagine/imageresizer)













