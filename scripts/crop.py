#!/usr/bin/env python3
"""
Image cropping script for rock specimen photos.
Crops images to 16:12 aspect ratio from the center.

Usage:
    python scripts/crop.py input_image.jpg                 # saves to ./cropped/input_image.jpg
    python scripts/crop.py input_image.jpg output.jpg      # saves to specified path
    python scripts/crop.py *.jpg                           # batch process to ./cropped/
"""

import sys
import os
from PIL import Image
import argparse


def crop_to_16_10(image_path, output_path=None, quality=95):
    """
    Crop an image to 16:12 aspect ratio from the center.
    
    Args:
        image_path (str): Path to input image
        output_path (str): Path for output image (optional, defaults to ./cropped/)
        quality (int): JPEG quality (1-100)
    
    Returns:
        str: Path to the output file
    """
    try:
        # Open the image without applying EXIF rotation
        img = Image.open(image_path)
        
        # Prevent automatic EXIF orientation by creating a copy without EXIF data
        # This ensures the image stays in its original orientation
        if hasattr(img, 'getexif') and img.getexif():
            # Create a new image without EXIF data to prevent rotation
            img_data = img.copy()
            img.close()
            img = img_data
        
        # Rotate image 90 degrees clockwise to correct orientation
        img = img.rotate(-90, expand=True)
        print("🔄 Rotated image 90° clockwise")
        
        # Get original dimensions (after rotation correction)
        original_width, original_height = img.size
        print(f"Original size (after rotation): {original_width}x{original_height}")
        
        # Calculate 16:12 aspect ratio
        target_ratio = 16 / 12  # 1.333...
        current_ratio = original_width / original_height
        
        print(f"Current ratio: {current_ratio:.3f}, Target ratio: {target_ratio:.3f}")
        
        # Determine output path
        if output_path is None:
            # Create cropped directory if it doesn't exist
            cropped_dir = "./cropped"
            os.makedirs(cropped_dir, exist_ok=True)
            
            # Extract filename and create output path
            filename = os.path.basename(image_path)
            output_path = os.path.join(cropped_dir, filename)
        
        if abs(current_ratio - target_ratio) < 0.01:
            print("Image already has 16:12 aspect ratio!")
            if output_path != image_path:
                img.save(output_path, quality=quality, optimize=True)
                print(f"✅ Copied to: {output_path}")
                img.close()
                return output_path
            img.close()
            return image_path
        
        # Calculate crop dimensions
        if current_ratio > target_ratio:
            # Image is too wide, crop width
            new_width = int(original_height * target_ratio)
            new_height = original_height
            left = (original_width - new_width) // 2
            top = 0
            right = left + new_width
            bottom = original_height
        else:
            # Image is too tall, crop height
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - new_height) // 2
            right = original_width
            bottom = top + new_height
        
        print(f"Cropping to: {new_width}x{new_height}")
        print(f"Crop box: ({left}, {top}, {right}, {bottom})")
        
        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))
        
        # Save the cropped image
        if cropped_img.mode == 'RGBA' and output_path.lower().endswith('.jpg'):
            # Convert RGBA to RGB for JPEG
            background = Image.new('RGB', cropped_img.size, (255, 255, 255))
            background.paste(cropped_img, mask=cropped_img.split()[-1])
            cropped_img = background
        
        cropped_img.save(output_path, quality=quality, optimize=True)
        print(f"✅ Cropped image saved to: {output_path}")
        
        # Clean up
        img.close()
        cropped_img.close()
        
        return output_path
            
    except FileNotFoundError:
        print(f"❌ Error: File '{image_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Crop images to 16:12 aspect ratio for rock specimen photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/crop.py photo.jpg                    # Save to ./cropped/photo.jpg
  python scripts/crop.py photo.jpg cropped.jpg        # Save to specific file
  python scripts/crop.py photo.jpg -q 85              # Lower quality, save to ./cropped/
  python scripts/crop.py *.jpg                        # Batch process to ./cropped/
        """
    )
    
    parser.add_argument('input_files', nargs='+', help='Input image file(s)')
    parser.add_argument('output_file', nargs='?', help='Output file (optional, for single file only)')
    parser.add_argument('-q', '--quality', type=int, default=95, 
                       help='JPEG quality (1-100, default: 95)')
    
    args = parser.parse_args()
    
    # Validate quality
    if not 1 <= args.quality <= 100:
        print("❌ Quality must be between 1 and 100")
        sys.exit(1)
    
    # Handle multiple files
    if len(args.input_files) > 1:
        if args.output_file:
            print("❌ Cannot specify output file when processing multiple inputs")
            sys.exit(1)
        
        print(f"📸 Processing {len(args.input_files)} files...")
        print(f"📁 Output will be saved to: ./cropped/")
        
        # Create cropped directory if it doesn't exist
        cropped_dir = "./cropped"
        os.makedirs(cropped_dir, exist_ok=True)
        
        success_count = 0
        
        for input_file in args.input_files:
            print(f"\n🔄 Processing: {input_file}")
            # For batch processing, save to cropped directory
            filename = os.path.basename(input_file)
            output_path = os.path.join(cropped_dir, filename)
            result = crop_to_16_10(input_file, output_path, quality=args.quality)
            if result:
                success_count += 1
        
        print(f"\n✅ Successfully processed {success_count}/{len(args.input_files)} files")
        print(f"📁 All cropped images saved to: {cropped_dir}/")
    
    # Handle single file
    else:
        input_file = args.input_files[0]
        output_file = args.output_file
        
        print(f"🔄 Processing: {input_file}")
        result = crop_to_16_10(input_file, output_file, quality=args.quality)
        
        if result:
            print("✅ Done!")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
