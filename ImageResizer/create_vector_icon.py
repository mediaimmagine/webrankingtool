"""
Create high-resolution vector-based icon inspired by trieste-news geometric design
Draws geometric shapes at very high resolution for crisp results
"""
from PIL import Image, ImageDraw
import os

def create_rounded_rectangle_mask(size, corner_radius):
    """Create a rounded rectangle mask"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], corner_radius, fill=255)
    return mask

def create_trieste_icon(size=1024):
    """
    Create geometric icon based on trieste-news design:
    - Orange and reddish-brown background
    - White geometric bird/arrow shape
    - Rounded corners
    """
    # Colors from the original icon
    ORANGE = (255, 138, 0)  # Bright orange
    BROWN = (139, 69, 19)   # Reddish-brown
    WHITE = (255, 255, 255)
    
    # Create base image
    img = Image.new('RGB', (size, size), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Corner radius (proportional to size)
    corner_radius = int(size * 0.08)
    
    # Draw rounded rectangle background split diagonally
    # Left side: darker brown triangle
    points_brown = [(0, 0), (0, size), (size * 0.45, size * 0.5)]
    draw.polygon(points_brown, fill=BROWN)
    
    # Right side: orange
    points_orange = [(size, 0), (size, size), (size * 0.45, size * 0.5)]
    draw.polygon(points_orange, fill=ORANGE)
    
    # Draw white geometric bird/arrow shape in center
    # Main body - large triangle pointing right
    center_x = size * 0.45
    center_y = size * 0.5
    
    # White arrow/bird shape (geometric)
    white_shape = [
        (center_x - size * 0.15, center_y - size * 0.2),  # Top left
        (center_x + size * 0.2, center_y),                 # Right point
        (center_x - size * 0.15, center_y + size * 0.2),   # Bottom left
    ]
    draw.polygon(white_shape, fill=WHITE)
    
    # Add small triangle for depth (wing/fold effect)
    small_triangle = [
        (center_x - size * 0.15, center_y + size * 0.08),
        (center_x + size * 0.05, center_y + size * 0.18),
        (center_x - size * 0.15, center_y + size * 0.2),
    ]
    draw.polygon(small_triangle, fill=(245, 245, 245))  # Slightly off-white for depth
    
    # Apply rounded corners mask
    mask = create_rounded_rectangle_mask((size, size), corner_radius)
    img.putalpha(mask)
    
    return img

# Generate icon at very high resolution
print("Creating high-resolution vector icon...")
icon_hires = create_trieste_icon(size=1024)

# Save high-res version for reference
icon_hires.save("mediaimmagine_icon_vector.png")
print(f"High-res preview saved: mediaimmagine_icon_vector.png (1024x1024)")

# Create ICO file with multiple sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icon_images = []

for size in icon_sizes:
    # Resize from high-res version for best quality
    icon = icon_hires.copy()
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Convert to RGB for ICO format
    icon_rgb = Image.new('RGB', size, (255, 255, 255))
    
    # Center the icon if needed
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

print("Icon created successfully: mediaimmagine_icon.ico")
print(f"  - Vector-based geometric design")
print(f"  - Rendered at 1024x1024 then scaled down")
print(f"  - Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
print("  - Sharp and crisp at all sizes!")




