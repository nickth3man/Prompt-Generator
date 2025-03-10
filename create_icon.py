from PIL import Image, ImageDraw, ImageFont
import os

# Create a blank image with transparent background
size = 256
image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a circular background
circle_color = (70, 130, 180, 255)  # Steel blue
draw.ellipse((0, 0, size, size), fill=circle_color)

# Add the question mark symbol
try:
    # Try to use a system font
    font = ImageFont.truetype("Arial", 180)
except IOError:
    # Fallback to default
    font = ImageFont.load_default()

# Draw the question mark in white
text = "?"
text_color = (255, 255, 255, 255)  # White

# Calculate text position to center it
# Updated for newer Pillow versions
try:
    # For newer Pillow versions
    left, top, right, bottom = font.getbbox(text)
    text_width = right - left
    text_height = bottom - top
except AttributeError:
    try:
        # For older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)
    except AttributeError:
        # Fallback method
        text_width, text_height = 100, 100  # Approximate size

position = ((size - text_width) // 2, (size - text_height) // 2 - 10)  # Adjust vertical position

# Draw the text
draw.text(position, text, font=font, fill=text_color)

# Save as .ico file
icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
image.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print(f"Icon created at: {icon_path}")
