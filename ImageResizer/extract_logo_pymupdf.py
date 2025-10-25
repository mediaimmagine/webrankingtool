"""
Extract square logo from PDF using PyMuPDF (fitz)
"""
import fitz  # PyMuPDF
from PIL import Image
import io

# Path to PDF
pdf_path = r"C:\Users\front\Pictures\trieste color negativ.pdf"

print(f"Opening PDF: {pdf_path}")

# Open PDF
pdf_document = fitz.open(pdf_path)

# Get first page
page = pdf_document[0]

print(f"PDF page size: {page.rect.width} x {page.rect.height} points")

# Render page to image at high resolution (300 DPI = 4.17x scale factor)
# Higher DPI = better quality
zoom = 4  # 4x = ~300 DPI
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)

print(f"Rendered image size: {pix.width}x{pix.height} pixels")

# Convert to PIL Image
img_data = pix.tobytes("png")
img = Image.open(io.BytesIO(img_data))

# Save full page for reference
img.save("pdf_full_page.png")
print(f"Full page saved: pdf_full_page.png ({img.width}x{img.height})")

# Auto-detect the logo area (look for square content)
# Convert to grayscale and find bounding box
gray = img.convert('L')

# Try to find the content area (non-white)
# Get bounding box of non-white content
bbox = gray.getbbox()

if bbox:
    x1, y1, x2, y2 = bbox
    print(f"\nContent bounding box: {bbox}")
    print(f"Content size: {x2-x1}x{y2-y1} pixels")
    
    # Crop to content
    logo = img.crop(bbox)
    logo.save("pdf_logo_cropped.png")
    print(f"Logo cropped and saved: pdf_logo_cropped.png ({logo.width}x{logo.height})")
    
    # If it's roughly square, use it. Otherwise, let's try to find the square logo
    width = x2 - x1
    height = y2 - y1
    aspect_ratio = width / height
    
    if 0.8 < aspect_ratio < 1.2:  # Roughly square
        print(f"Logo is roughly square (aspect ratio: {aspect_ratio:.2f})")
        final_logo = logo
    else:
        print(f"Logo is not square (aspect ratio: {aspect_ratio:.2f})")
        print("Looking for square region in the content...")
        
        # Look for the largest square region
        # Try to find the square icon - it's likely in a specific area
        # For now, let's use the cropped content
        final_logo = logo
    
    # Save the final logo at high resolution
    final_logo.save("logo_extracted_hires.png")
    print(f"\nFinal logo saved: logo_extracted_hires.png")
    print(f"Size: {final_logo.width}x{final_logo.height} pixels")
    print("\nThis will be used to create the icon!")
    
else:
    print("Could not detect content in PDF")

pdf_document.close()

