"""
Convert mediaimmagine logo to ICO file for Windows executable
"""
from PIL import Image
import os

# Path to logo
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mediaimmagine_logo.png")

# Open and convert
img = Image.open(logo_path)

# Create multiple sizes for Windows icon (16x16, 32x32, 48x48, 256x256)
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save("mediaimmagine_icon.ico", format='ICO', sizes=icon_sizes)

print("Icon created successfully: mediaimmagine_icon.ico")

