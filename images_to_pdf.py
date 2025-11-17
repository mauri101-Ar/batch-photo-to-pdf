import os
import argparse
from datetime import datetime, date
from PIL import Image
from fpdf import FPDF
from natsort import natsorted
from image_processing import find_and_crop_presentation


def create_pdf_from_images(directory_path, orientation, today_only=False, smart_crop=False):
    """
    Creates a PDF from all images in a directory,
    ordered by creation/modification date.

    :param directory_path: Path to the directory containing images.
    :param orientation: 'P' (Portrait) or 'L' (Landscape).
    :param today_only: If True, only processes images modified today.
    :param smart_crop: If True, attempts to crop the main presentation area. # NEW PARAMETER
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return

    # 1. Get list of image files and their metadata
    image_files_with_stats = []
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

    current_date = date.today()

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(image_extensions):
            full_path = os.path.join(directory_path, filename)
            timestamp = os.path.getmtime(full_path)

            if today_only:
                file_date = datetime.fromtimestamp(timestamp).date()
                if file_date != current_date:
                    continue

            image_files_with_stats.append({
                'path': full_path,
                'timestamp': timestamp,
                'filename': filename
            })

    if not image_files_with_stats:
        if today_only:
            print(f"No images found in '{directory_path}' that were modified today ({current_date}).")
        else:
            print(f"No images found in directory '{directory_path}'.")
        return

    # 2. Sort images (same logic)
    sorted_images = sorted(
        image_files_with_stats,
        key=lambda x: (x['timestamp'], natsorted([x['filename']])[0])
    )

    # 3. PDF Setup (same logic)
    output_dir = "PDF"  # Name of the folder to save the output

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    directory_name = os.path.basename(os.path.abspath(directory_path))

    if today_only:
        output_filename = f"{directory_name}_today_{current_date.strftime('%Y%m%d')}.pdf"
    else:
        output_filename = f"{directory_name}_compiled.pdf"

    output_filename = os.path.join(output_dir, output_filename)

    # ... (PDF setup and dimension definitions are the same) ...
    pdf = FPDF(orientation.upper(), 'mm', 'A4')

    print(f"Starting PDF creation ('{orientation}' - 1 image per page)...")
    if smart_crop:
        print("Enabled smart cropping for presentation slides.")
    print(f"Total images to process: {len(sorted_images)}")

    # A4 dimensions in mm (210 x 297)
    if orientation.upper() == 'P':
        page_width, page_height = 210, 297
    else:  # 'L'
        page_width, page_height = 297, 210

    # Margins (e.g., 10mm all sides)
    margin = 10
    max_img_width = page_width - 2 * margin
    max_img_height = page_height - 2 * margin

    # Main processing loop
    for i, img_data in enumerate(sorted_images):
        img_path = img_data['path']

        try:
            if smart_crop:
                # Use the external function to get the cropped image (PIL object)
                img = find_and_crop_presentation(img_path)

                # If smart cropping failed, fall back to loading the original image
                if img is None:
                    img = Image.open(img_path)
            else:
                # Original logic: just load the image
                img = Image.open(img_path)

            img_w, img_h = img.size

            # Add a new page
            pdf.add_page()

            # Calculate scaling factor to fit image on page while maintaining aspect ratio
            ratio_w = max_img_width / img_w
            ratio_h = max_img_height / img_h

            scale_factor = min(ratio_w, ratio_h)

            # New dimensions and position (same centering logic)
            new_w = img_w * scale_factor
            new_h = img_h * scale_factor
            pos_x = (page_width - new_w) / 2
            pos_y = (page_height - new_h) / 2

            # Add image to PDF (fpdf handles PIL Image objects directly)
            pdf.image(img, x=pos_x, y=pos_y, w=new_w, h=new_h)

            print(f"  - Added page {i+1}/{len(sorted_images)}: {img_data['filename']}")

        except Exception as e:
            print(f"Warning: Could not process image '{img_path}'. Error: {e}")
            continue

    # 4. Save the PDF (Corrected call)
    pdf.output(output_filename)
    print("---")
    print(f"Success! PDF created and saved as: **{output_filename}**")
    print(f"Full Path: {os.path.abspath(output_filename)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a chronologically sorted PDF from images in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory containing the images."
    )
    parser.add_argument(
        "orientation",
        choices=['P', 'L', 'Portrait', 'Landscape'],
        help="Page orientation: 'P' or 'Portrait', 'L' or 'Landscape'."
    )
    parser.add_argument(
        "--today-only",
        action="store_true",
        help="If set, only process images that were modified on the current date."
    )
    parser.add_argument(
        "--smart-crop",
        action="store_true",
        help="If set, attempts to automatically detect and crop the main presentation area from screenshots."
    )

    args = parser.parse_args()

    orientation_map = {
        'P': 'P', 'p': 'P', 'Portrait': 'P',
        'L': 'L', 'l': 'L', 'Landscape': 'L'
    }

    orientation_code = orientation_map[args.orientation.lower()]

    create_pdf_from_images(args.directory, orientation_code, args.today_only, args.smart_crop)
