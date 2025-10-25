"""
Create high-quality icon from the extracted square logo
"""
from PIL import Image

# Open the extracted square logo
logo = Image.open("square_logo_extracted.png")
print(f"Using extracted logo: {logo.width}x{logo.height} pixels")

# Icon sizes to generate
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icon_images = []

for size in icon_sizes:
    # Resize the logo for this icon size
    icon = logo.copy()
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Convert to RGB for ICO format
    icon_rgb = Image.new('RGB', size, (255, 255, 255))
    
    # Center if needed
    x = (size[0] - icon.width) // 2
    y = (size[1] - icon.height) // 2
    
    if icon.mode == 'RGBA':
        icon_rgb.paste(icon, (x, y), icon)
    else:
        icon_rgb.paste(icon, (x, y))
    
    icon_images.append(icon_rgb)

# Save as ICO
icon_images[0].save(
    "mediaimmagine_icon.ico",
    format='ICO',
    sizes=icon_sizes,
    append_images=icon_images[1:]
)

print("\nIcon created successfully: mediaimmagine_icon.ico")
print(f"  - Source: Extracted square logo from PDF (942x942px)")
print(f"  - Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
print("  - High quality - scaled from extracted vector PDF!")



