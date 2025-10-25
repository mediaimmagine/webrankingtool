"""
Extract square logo from PDF and create high-quality icon
"""
from PIL import Image
from pdf2image import convert_from_path
import os

# Path to PDF
pdf_path = r"C:\Users\front\Pictures\trieste color negativ.pdf"

print(f"Converting PDF to high-resolution image: {pdf_path}")

# Convert PDF to images at high DPI (300 DPI for quality)
try:
    images = convert_from_path(pdf_path, dpi=300, fmt='png')
    
    if images:
        # Get the first page
        pdf_image = images[0]
        print(f"PDF converted to image: {pdf_image.width}x{pdf_image.height} pixels")
        
        # Save full PDF image for reference
        pdf_image.save("ImageResizer/pdf_full_page.png")
        print("Full PDF page saved as: pdf_full_page.png")
        
        # Now let's display info so we can crop the square logo
        print(f"\nPDF Image size: {pdf_image.width}x{pdf_image.height}")
        print("Please check pdf_full_page.png to locate the square logo")
        print("I'll try to auto-detect it by finding the brightest square region...")
        
        # Auto-detect square logo area (look for white/bright content)
        # This is a simple approach - find bounds of non-white content
        # Convert to grayscale to find content
        gray = pdf_image.convert('L')
        
        # Find bounding box of content (non-white areas)
        bbox = gray.getbbox()
        
        if bbox:
            print(f"Content detected at: {bbox}")
            
            # Try to find square regions - the logo is likely square
            # Let's extract different potential square crops
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            
            print(f"Content size: {width}x{height}")
            
            # Save the cropped region
            cropped = pdf_image.crop(bbox)
            cropped.save("ImageResizer/pdf_logo_extracted.png")
            print(f"Extracted logo saved as: pdf_logo_extracted.png")
            print(f"Size: {cropped.width}x{cropped.height}")
            
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: pdf2image requires poppler. On Windows, you may need to:")
    print("1. Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/")
    print("2. Extract it and add the 'bin' folder to your PATH")
    print("\nAlternatively, please export the square logo from the PDF as PNG at 2048x2048px")



