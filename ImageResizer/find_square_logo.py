"""
Find and extract the square logo from the PDF page
"""
from PIL import Image, ImageDraw
import numpy as np

# Open the extracted PDF page
img = Image.open("pdf_full_page.png")
print(f"Image size: {img.width}x{img.height}")

# Convert to RGB if needed
if img.mode != 'RGB':
    img = img.convert('RGB')

# Convert to numpy array for easier analysis
img_array = np.array(img)

# Strategy: Look for square regions with distinct colors
# The trieste logo has orange and brown colors

# First, let's look for regions with significant color variance
# (logos typically have distinct colors vs white background)

# Calculate where there's actual content (non-white areas)
# Consider a pixel "white" if all RGB values are > 250
white_threshold = 250
is_white = np.all(img_array > white_threshold, axis=2)
is_content = ~is_white

# Find rows and columns that contain content
rows_with_content = np.any(is_content, axis=1)
cols_with_content = np.any(is_content, axis=0)

if np.any(rows_with_content) and np.any(cols_with_content):
    # Find the bounding box of all content
    row_indices = np.where(rows_with_content)[0]
    col_indices = np.where(cols_with_content)[0]
    
    top = row_indices[0]
    bottom = row_indices[-1]
    left = col_indices[0]
    right = col_indices[-1]
    
    print(f"Content found at: left={left}, top={top}, right={right}, bottom={bottom}")
    print(f"Content dimensions: {right-left}x{bottom-top}")
    
    # Now let's look for square regions
    # Scan the content area for concentrated square blocks
    content_width = right - left
    content_height = bottom - top
    
    # The logo is likely one of the distinct square regions
    # Let's try to find regions with orange/brown colors
    
    # Look for orange pixels (R > 200, G > 100, B < 50)
    is_orange = (img_array[:,:,0] > 200) & (img_array[:,:,1] > 100) & (img_array[:,:,1] < 160) & (img_array[:,:,2] < 50)
    
    if np.any(is_orange):
        # Find bounding box of orange content
        rows_with_orange = np.any(is_orange, axis=1)
        cols_with_orange = np.any(is_orange, axis=0)
        
        if np.any(rows_with_orange) and np.any(cols_with_orange):
            row_idx = np.where(rows_with_orange)[0]
            col_idx = np.where(cols_with_orange)[0]
            
            logo_top = row_idx[0]
            logo_bottom = row_idx[-1]
            logo_left = col_idx[0]
            logo_right = col_idx[-1]
            
            print(f"\nOrange region (likely logo) found at:")
            print(f"  left={logo_left}, top={logo_top}, right={logo_right}, bottom={logo_bottom}")
            print(f"  Size: {logo_right-logo_left}x{logo_bottom-logo_top}")
            
            # Add some padding and make it square
            logo_width = logo_right - logo_left
            logo_height = logo_bottom - logo_top
            logo_size = max(logo_width, logo_height)
            
            # Add 10% padding
            padding = int(logo_size * 0.1)
            logo_size += padding * 2
            
            # Center the crop
            center_x = (logo_left + logo_right) // 2
            center_y = (logo_top + logo_bottom) // 2
            
            crop_left = max(0, center_x - logo_size // 2)
            crop_top = max(0, center_y - logo_size // 2)
            crop_right = min(img.width, crop_left + logo_size)
            crop_bottom = min(img.height, crop_top + logo_size)
            
            # Crop the square logo
            logo = img.crop((crop_left, crop_top, crop_right, crop_bottom))
            logo.save("square_logo_extracted.png")
            print(f"\nSquare logo extracted and saved: square_logo_extracted.png")
            print(f"Final size: {logo.width}x{logo.height} pixels")
        else:
            print("Could not find orange region bounds")
    else:
        print("Could not find orange colors in the image")
        print("The full content will be saved instead")
        cropped = img.crop((left, top, right, bottom))
        cropped.save("square_logo_extracted.png")
        print(f"Content saved: square_logo_extracted.png ({cropped.width}x{cropped.height})")
else:
    print("Could not find any content in the image")



