import cv2
from PIL import Image


def find_and_crop_presentation(image_path: str) -> Image.Image | None:
    """
    Tries to find the main presentation screen within a screenshot
    (like from Zoom or Meet) and crops the image to that area.

    :param image_path: Path to the image file.
    :return: A PIL Image object of the cropped area, or None if detection fails.
    """
    try:
        # Load the image using OpenCV
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            print(f"  [Processor] Warning: Could not load image {image_path} with OpenCV.")
            return None

        # 1. Preprocessing
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        # Apply slight blur to smooth edges and reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 2. Edge Detection (Canny)
        edged = cv2.Canny(blurred, 50, 150)

        # 3. Find Contours
        # RETR_EXTERNAL retrieves only the extreme outer contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 4. Filter and Find the Best Candidate (the Presentation)
        # Determine the minimum size threshold (e.g., 20% of the image area)
        min_area = img_cv.shape[0] * img_cv.shape[1] * 0.20

        best_rect = None
        max_area = 0

        for c in contours:
            # Approximate the contour shape to simplify it (e.g., to a polygon with 4 sides)
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

            area = cv2.contourArea(c)

            # Check if the contour is a quadrilateral (4 sides) and is large enough
            if len(approx) >= 4 and area > min_area:
                x, y, w, h = cv2.boundingRect(c)

                # Simple aspect ratio check (slides are usually 16:9 or 4:3, or similar)
                aspect_ratio = w / h

                # Prioritize rectangles that are large and reasonably rectangular (e.g., 0.8 to 2.5)
                if area > max_area and 0.5 < aspect_ratio < 3.0:
                    max_area = area
                    best_rect = (x, y, w, h)

        if best_rect:
            x, y, w, h = best_rect

            # 5. Crop the image
            cropped_cv = img_cv[y:y + h, x:x + w]

            # Convert the cropped OpenCV image (BGR) to a PIL Image (RGB)
            cropped_pil = Image.fromarray(cv2.cvtColor(cropped_cv, cv2.COLOR_BGR2RGB))
            print(f"  [Processor] Success: Cropped image from {img_cv.shape} to {cropped_cv.shape}")
            return cropped_pil
        else:
            print(f"  [Processor] Warning: No suitable presentation area found in {image_path}.")
            return None  # Return None to signal that cropping failed

    except Exception as e:
        print(f"  [Processor] Error during image processing: {e}")
        return None
