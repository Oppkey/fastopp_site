#!/usr/bin/env python3
"""
Script to create favicon files from the FastOpp logo.
This script converts the existing logo to various favicon formats.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_favicon():
    """Create favicon files from the FastOpp logo."""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    logo_path = project_root / "static" / "images" / "fastopp_logo.webp"
    static_dir = project_root / "static"
    
    # Check if logo exists
    if not logo_path.exists():
        print(f"Error: Logo file not found at {logo_path}")
        return False
    
    try:
        # Open the logo image
        with Image.open(logo_path) as img:
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create favicon.ico (16x16, 32x32, 48x48)
            favicon_sizes = [16, 32, 48]
            favicon_images = []
            
            for size in favicon_sizes:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                favicon_images.append(resized)
            
            # Save favicon.ico
            favicon_path = static_dir / "favicon.ico"
            favicon_images[0].save(
                favicon_path,
                format='ICO',
                sizes=[(size, size) for size in favicon_sizes],
                append_images=favicon_images[1:]
            )
            print(f"Created favicon.ico at {favicon_path}")
            
            # Create PNG favicon (32x32)
            png_favicon_path = static_dir / "favicon-32x32.png"
            favicon_images[1].save(png_favicon_path, format='PNG')
            print(f"Created favicon-32x32.png at {png_favicon_path}")
            
            # Create Apple touch icon (180x180)
            apple_touch_path = static_dir / "apple-touch-icon.png"
            apple_touch = img.resize((180, 180), Image.Resampling.LANCZOS)
            apple_touch.save(apple_touch_path, format='PNG')
            print(f"Created apple-touch-icon.png at {apple_touch_path}")
            
            # Create a simple text-based favicon as fallback
            create_text_favicon(static_dir)
            
            return True

    except Exception as e:
        print(f"Error creating favicon: {e}")
        return False


def create_text_favicon(static_dir):
    """Create a simple text-based favicon as fallback."""
    try:
        # Create a 32x32 image with a blue background
        img = Image.new('RGBA', (32, 32), (59, 130, 246, 255))  # AI blue color
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            # Try to use a system font
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        except OSError:
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
                )
            except OSError:
                font = ImageFont.load_default()
        
        # Draw "F" for FastOpp
        text = "F"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (32 - text_width) // 2
        y = (32 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # Save as fallback favicon
        fallback_path = static_dir / "favicon-fallback.png"
        img.save(fallback_path, format='PNG')
        print(f"Created fallback favicon at {fallback_path}")
        
    except Exception as e:
        print(f"Error creating fallback favicon: {e}")


if __name__ == "__main__":
    success = create_favicon()
    if success:
        print("Favicon creation completed successfully!")
    else:
        print("Favicon creation failed!")
        sys.exit(1)
