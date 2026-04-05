"""OpenCV-based mask overlay and geometry helpers."""

from __future__ import annotations

from typing import List, Sequence, Tuple

import cv2
import numpy as np


def mask_area_from_binary(mask: np.ndarray) -> float:
    """Area in pixels from a binary mask (H, W), values 0/1 or 0/255."""
    if mask.dtype != np.uint8:
        m = (mask > 0).astype(np.uint8) * 255
    else:
        m = mask
    return float(cv2.countNonZero(m))


def mask_area_from_polygon(
    polygon_xy: np.ndarray,
    image_shape: Tuple[int, int],
) -> float:
    """Rasterize polygon to mask and return pixel area. image_shape is (height, width)."""
    h, w = image_shape
    mask = np.zeros((h, w), dtype=np.uint8)
    pts = np.round(polygon_xy).astype(np.int32).reshape(-1, 1, 2)
    cv2.fillPoly(mask, [pts], 255)
    return float(cv2.countNonZero(mask))


def contour_area_from_polygon(polygon_xy: np.ndarray) -> float:
    """Shoelace / OpenCV contour area for closed polygon in pixel coordinates."""
    pts = np.round(polygon_xy).astype(np.float32).reshape(-1, 1, 2)
    return float(cv2.contourArea(pts))


def distinct_colors(n: int, saturation: int = 255, value: int = 255) -> List[Tuple[int, int, int]]:
    """Generate n highly distinct BGR colors using HSV wheel."""
    if n <= 0:
        return []
    colors: List[Tuple[int, int, int]] = []
    for i in range(n):
        hue = int(180 * i / max(n, 1)) % 180
        hsv = np.uint8([[[hue, saturation, value]]])
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0]
        colors.append((int(bgr[0]), int(bgr[1]), int(bgr[2])))
    return colors


def overlay_instance_masks(
    image_bgr: np.ndarray,
    masks: Sequence[np.ndarray],
    alpha: float = 0.45,
) -> np.ndarray:
    """
    Overlay binary masks with distinct colors on a BGR image.

    Each mask is (H, W) with nonzero = foreground. Masks must match image dimensions.
    """
    out = image_bgr.copy()
    if not masks:
        return out
    colors = distinct_colors(len(masks))
    overlay = np.zeros_like(out)
    for i, m in enumerate(masks):
        if m.shape[:2] != out.shape[:2]:
            m = cv2.resize(m.astype(np.uint8), (out.shape[1], out.shape[0]), interpolation=cv2.INTER_NEAREST)
        bin_mask = (m > 0).astype(np.uint8)
        color = colors[i]
        for c in range(3):
            overlay[:, :, c] = np.where(bin_mask > 0, color[c], overlay[:, :, c])
    blended = cv2.addWeighted(overlay, alpha, out, 1.0 - alpha, 0)
    # Keep original pixels visible where no mask
    combined_mask = np.zeros(out.shape[:2], dtype=np.uint8)
    for m in masks:
        if m.shape[:2] != out.shape[:2]:
            m = cv2.resize(m.astype(np.uint8), (out.shape[1], out.shape[0]), interpolation=cv2.INTER_NEAREST)
        combined_mask = np.maximum(combined_mask, (m > 0).astype(np.uint8) * 255)
    for c in range(3):
        blended[:, :, c] = np.where(combined_mask > 0, blended[:, :, c], out[:, :, c])
    return blended


def draw_mask_boundaries(
    image_bgr: np.ndarray,
    masks: Sequence[np.ndarray],
    thickness: int = 2,
) -> np.ndarray:
    """Draw contour boundaries for each mask for extra visibility."""
    out = image_bgr.copy()
    colors = distinct_colors(len(masks))
    for i, m in enumerate(masks):
        if m.shape[:2] != out.shape[:2]:
            m = cv2.resize(m.astype(np.uint8), (out.shape[1], out.shape[0]), interpolation=cv2.INTER_NEAREST)
        bin_mask = (m > 0).astype(np.uint8) * 255
        contours, _ = cv2.findContours(bin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, colors[i], thickness)
    return out
