"""
Convert mediaimmagine logo to ICO file for Windows executable
Creates icon with red background matching the brand, without stretching the logo
Uses vector EPS file for maximum sharpness
"""
from PIL import Image, ImageDraw
import os

# Use trieste-news icon as base
icon_source = r"C:\Users\front\Pictures\trieste-news-icon-300x300.jpg"

print(f"Using icon source: {icon_source}")
logo = Image.open(icon_source).convert("RGBA")
print(f"Icon loaded at {logo.width}x{logo.height} pixels")

# Icon sizes to generate
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Create list to hold all icon versions
icon_images = []

for size in icon_sizes:
    # Create icon by resizing the trieste-news icon
    icon = logo.copy()
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Convert to RGB for ICO format
    icon_rgb = Image.new('RGB', size, (255, 255, 255))
    
    # Center the icon if it's not perfectly square after thumbnail
    x = (size[0] - icon.width) // 2
    y = (size[1] - icon.height) // 2
    
    if icon.mode == 'RGBA':
        icon_rgb.paste(icon, (x, y), icon)
    else:
        icon_rgb.paste(icon, (x, y))
    
    icon_images.append(icon_rgb)

# Save as ICO with all sizes
icon_images[0].save(
    "mediaimmagine_icon.ico", 
    format='ICO', 
    sizes=icon_sizes,
    append_images=icon_images[1:]
)

print("Icon created successfully: mediaimmagine_icon.ico")
print(f"  - Source: trieste-news-icon-300x300.jpg")
print(f"  - Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")

