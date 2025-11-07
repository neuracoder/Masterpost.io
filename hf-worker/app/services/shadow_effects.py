"""
Shadow Effects Module for Masterpost Worker
Simplified version for HF Spaces deployment
"""

from PIL import Image, ImageFilter
import logging

logger = logging.getLogger(__name__)

def apply_simple_drop_shadow(image, intensity=0.5):
    """
    Simplified drop shadow - optimized for performance

    Args:
        image: PIL Image with RGBA (transparent background)
        intensity: Shadow darkness 0.0-1.0

    Returns:
        PIL Image with drop shadow on white background
    """
    logger.info(f"[SHADOW] Applying drop shadow, intensity={intensity}")

    try:
        # Ensure RGBA mode
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        width, height = image.size

        # Shadow parameters (fixed for simplicity and performance)
        offset_x = 15
        offset_y = 15
        blur_radius = 20

        # Create expanded canvas for shadow
        padding = blur_radius + offset_x + offset_y
        shadow_size = (width + padding * 2, height + padding * 2)

        # Extract alpha channel for shadow mask
        alpha = image.split()[3]

        # Create shadow layer
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        shadow_alpha = alpha.point(lambda x: int(x * intensity) if x > 10 else 0)
        shadow.paste((100, 100, 100, 255), (0, 0), shadow_alpha)

        # Apply Gaussian blur to shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # Create final canvas with WHITE background
        result = Image.new('RGB', shadow_size, (255, 255, 255))

        # Position shadow with offset
        shadow_x = padding + offset_x
        shadow_y = padding + offset_y

        # Paste shadow (convert to RGB for white background)
        shadow_rgb = Image.new('RGB', shadow.size, (255, 255, 255))
        shadow_rgb.paste(shadow, mask=shadow.split()[3] if shadow.mode == 'RGBA' else None)
        result.paste(shadow_rgb, (shadow_x, shadow_y))

        # Paste original product on top of shadow
        result.paste(image, (padding, padding), image)

        logger.info(f"✓ Shadow applied successfully, result size: {result.size}")
        return result

    except Exception as e:
        logger.error(f"Shadow application failed: {e}")
        # Return image on white background as fallback
        fallback = Image.new('RGB', image.size, (255, 255, 255))
        fallback.paste(image, (0, 0), image if image.mode == 'RGBA' else None)
        return fallback
