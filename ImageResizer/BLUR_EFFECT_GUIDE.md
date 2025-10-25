# 🌫️ Blur Effect Feature Guide

## Overview

The blur effect feature allows you to convert vertical/portrait images to horizontal/landscape formats without cropping or stretching. Instead, the image is centered on a beautifully blurred background created from the image itself.

This is a popular technique used on social media platforms like Instagram, TikTok, and Facebook when you want to post a portrait image in a landscape format.

---

## When to Use Blur Effect

### ✅ Perfect For:
- **Vertical images → Horizontal formats**
  - Example: 1080x1350 (Instagram Post) → 1920x1080 (Full HD)
  - Example: 1080x1920 (Instagram Story) → 1920x1080 (YouTube Thumbnail)

### ❌ Not Available For:
- Horizontal images → Vertical formats (use crop instead)
- Same aspect ratio conversions
- When "Crop to fit" is enabled (mutually exclusive)

---

## How It Works

### Step-by-Step Guide

1. **Upload a Vertical Image**
   - Click "📁 Upload Image"
   - Select a portrait/vertical image

2. **Select a Horizontal Preset**
   - Choose: Full HD (1920x1080), 2K (2048x1366), or HD (1280x720)
   - The blur option will automatically become available

3. **Enable Blur Effect**
   - Check: "🌫️ Add blur effect on sides"
   - A blur strength slider will appear

4. **Adjust Blur Strength** (5-50)
   - **Low (5-15)**: Subtle blur, more detail visible
   - **Medium (20-30)**: Balanced blur (recommended)
   - **High (35-50)**: Heavy blur, very soft background

5. **Preview and Save**
   - Click "🔄 Update Preview" to see the result
   - Adjust blur strength if needed
   - Click "💾 Save Resized Image"

---

## Example Use Cases

### Instagram Story → YouTube Thumbnail
- **Original**: 1080x1920 (vertical story)
- **Target**: 1920x1080 (landscape thumbnail)
- **Blur Strength**: 25 (medium)
- **Result**: Centered story with blurred sides

### Instagram Post → Blog Header
- **Original**: 1080x1350 (Instagram portrait)
- **Target**: 2048x1366 (2K header)
- **Blur Strength**: 30 (medium-high)
- **Result**: Professional header with artistic blur

### Portrait Photo → Facebook Cover
- **Original**: 3000x4000 (portrait photo)
- **Target**: 1920x1080 (cover photo)
- **Blur Strength**: 20 (subtle)
- **Result**: Full photo centered, blurred edges

---

## Visual Example

```
BEFORE (1080x1920):           AFTER (1920x1080):
┌──────────┐                  ┌────────────────────────┐
│          │                  │🌫️ │          │ 🌫️│
│          │                  │🌫️ │          │ 🌫️│
│  PHOTO   │        →         │🌫️ │  PHOTO   │ 🌫️│
│          │                  │🌫️ │          │ 🌫️│
│          │                  │🌫️ │          │ 🌫️│
└──────────┘                  └────────────────────────┘
   VERTICAL                    HORIZONTAL WITH BLUR SIDES
```

---

## Technical Details

### How Blur is Applied

1. **Background Creation**
   - Original image is stretched to fill target dimensions
   - Gaussian blur filter is applied based on strength

2. **Image Centering**
   - Original image is scaled to fit within target dimensions
   - Aspect ratio is preserved
   - Image is centered on the blurred background

3. **Compositing**
   - Blurred background fills entire canvas
   - Sharp, centered image is placed on top
   - Result is seamless and professional

### Blur Strength Values

| Strength | Blur Radius | Effect | Best For |
|----------|-------------|--------|----------|
| 5-10 | Low | Subtle, details visible | Detailed backgrounds |
| 15-25 | Medium | Balanced blur | General use (recommended) |
| 30-40 | High | Strong blur | Busy backgrounds |
| 45-50 | Very High | Maximum blur | Distracting backgrounds |

---

## Tips for Best Results

### 1. **Choose Appropriate Blur Strength**
   - **Simple backgrounds**: Lower blur (10-20)
   - **Busy backgrounds**: Higher blur (30-40)
   - **Default sweet spot**: 25

### 2. **Color Harmony**
   - Works best when image colors are cohesive
   - Creates pleasing color gradients on sides

### 3. **Subject Positioning**
   - Center-focused images work best
   - Subjects at edges may blend with blur

### 4. **Format Selection**
   - Use JPG for photos (smaller file size)
   - Use PNG if transparency matters
   - Use WebP for modern web (best compression)

---

## Comparison: Blur vs Crop vs Stretch

### Blur Effect
✅ No content loss
✅ Artistic appearance
✅ Professional look
⚠️ Larger file size than crop

### Crop Mode
✅ Clean, sharp edges
✅ Smaller file size
❌ Loses parts of image
❌ May cut important content

### Stretch (Default)
✅ All content visible
✅ Fastest processing
❌ Distorted proportions
❌ Unprofessional look

---

## Keyboard Shortcuts & Quick Actions

- **Preview Updates**: Automatically after 300ms when adjusting blur
- **Manual Preview**: Click "🔄 Update Preview"
- **Toggle On/Off**: Check/uncheck blur effect to compare

---

## Troubleshooting

### "Blur option is grayed out"
- ✅ Make sure aspect ratios differ
- ✅ Uncheck "Crop to fit" mode
- ✅ Use portrait → landscape conversion

### "Blur looks pixelated"
- ✅ Use higher quality setting (85%+)
- ✅ Reduce blur strength
- ✅ Use PNG format instead of JPG

### "Blur doesn't show in preview"
- ✅ Click "🔄 Update Preview" manually
- ✅ Wait 300ms after adjusting slider
- ✅ Make sure blur is checked ✓

---

## Advanced Techniques

### Creating Gradient Backgrounds
1. Upload image with solid/gradient background
2. Apply high blur (40-50)
3. Creates smooth color gradient effect

### Minimalist Look
1. Upload image with simple background
2. Apply low blur (5-10)
3. Subtle, elegant result

### Bokeh Effect
1. Upload image with lights in background
2. Apply medium-high blur (30-40)
3. Lights create bokeh circles

---

## Performance Notes

- **Processing Time**: Adds ~200-500ms vs regular resize
- **File Size**: Similar to crop mode
- **Memory Usage**: Minimal increase
- **Preview Speed**: Real-time with 300ms debounce

---

## Examples by Platform

### YouTube Thumbnails
- **Size**: 1920x1080
- **Blur**: 25-30
- **Quality**: 85%
- **Format**: JPG

### Facebook Covers
- **Size**: 1920x1080
- **Blur**: 20-25
- **Quality**: 80%
- **Format**: JPG

### Website Banners
- **Size**: 2048x1366
- **Blur**: 15-25
- **Quality**: 85%
- **Format**: WebP or JPG

### Twitter Headers
- **Size**: 1500x500 (custom)
- **Blur**: 25-30
- **Quality**: 80%
- **Format**: JPG

---

## Conclusion

The blur effect feature gives you a professional way to convert vertical images to horizontal formats without losing content or creating distortion. Experiment with different blur strengths to find what works best for your images!

**Happy editing!** 🎨✨

