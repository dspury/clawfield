"""Utilities for image download and path management."""

import os
import urllib.request
from pathlib import Path
from typing import Optional


def get_output_dir(fallback: str = "./assets") -> Path:
    """
    Determine output directory for downloaded images.
    Priority:
    1. HF_OUTPUT_DIR env var
    2. XDG_DATA_HOME/clawfield
    3. fallback (./assets)
    """
    if env_dir := os.getenv("HF_OUTPUT_DIR"):
        return Path(env_dir)
    
    if xdg_data := os.getenv("XDG_DATA_HOME"):
        path = Path(xdg_data) / "clawfield"
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    path = Path(fallback)
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_image(
    url: str,
    output_path: Optional[Path] = None,
    filename: Optional[str] = None,
) -> Path:
    """
    Download image from URL to local path.
    
    Args:
        url: Image URL from Higgsfield API
        output_path: Directory to save (defaults to ./assets/ via get_output_dir)
        filename: Optional filename (defaults to timestamp + .png)
    
    Returns:
        Path to downloaded file
    
    Raises:
        IOError: If download fails
    """
    if output_path is None:
        output_path = get_output_dir()
    
    if filename is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
    
    full_path = output_path / filename
    
    try:
        urllib.request.urlretrieve(url, str(full_path))
        return full_path
    except Exception as e:
        raise IOError(f"Failed to download image from {url}: {e}")


def format_size(bytes_count: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB"]:
        if abs(bytes_count) < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} GB"
