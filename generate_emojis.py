import os
from PIL import Image, ImageDraw, ImageFont

def generate_emoji_images(emojis, output_dir="output", size=1024):
    """
    Generates images for a list of emojis, ensuring they are perfectly centered.
    This method uses a two-pass approach:
    1. Render the emoji to a large transparent canvas to find its true bounding box.
    2. Crop and paste it centered onto the final image.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    font_path = r"C:\Windows\Fonts\seguiemj.ttf"
    font_size = 800
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    for i, emoji in enumerate(emojis):
        # 1. First Pass: Render emoji to find its tight bounding box
        # We use size*2 to ensure the emoji isn't clipped by any default font offsets
        temp_size = size * 2
        temp_img = Image.new('RGBA', (temp_size, temp_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Draw emoji in the middle of our large scratchpad
        # embedded_color=True is required for Segoe UI Emoji to render in color
        temp_draw.text((temp_size // 2, temp_size // 2), emoji, font=font, anchor="mm", embedded_color=True)
        
        # getbbox() finds the bounding box of non-zero (non-transparent) pixels
        bbox = temp_img.getbbox()
        
        # 2. Second Pass: Create final centered image
        img = Image.new('RGB', (size, size), color='white')
        
        if bbox:
            # Crop exactly around the emoji pixels
            emoji_crop = temp_img.crop(bbox)
            w, h = emoji_crop.size
            
            # Calculate coordinates to place the center of the crop at the center of our image
            paste_x = (size - w) // 2
            paste_y = (size - h) // 2
            
            # Use the crop itself as a mask to preserve transparency
            img.paste(emoji_crop, (paste_x, paste_y), emoji_crop)
            print(f"Generated emoji_{i}.png for {emoji} (centered {w}x{h})")
        else:
            print(f"Warning: No visible pixels for {emoji}. Generating blank image.")
        
        # Save the final image
        filename = f"emoji_{i}.png"
        img.save(os.path.join(output_dir, filename))

if __name__ == "__main__":
    emoji_list = [
        "🌳", # tree
        "🔥", # fire
        "📁", # file/file cabinet
        "🌃", # city at night
        "🎅", # santa hat
        "🙂", # smiley face
        "🅰️", # letter A (often problematic with variation selectors)
        "🎤", # microphone
        "🚜", # tractor
        "🔁", # replay
        "🍾"  # bottle
    ]
    generate_emoji_images(emoji_list)
