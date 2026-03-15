"""clawfield package exports."""

__version__ = "0.1.0"

from .client import (
    HiggsfieldClient,
    ClawfieldError,
    AuthError,
    RateLimitError,
    InvalidModelError,
)
from .builder import BuildRequest, PromptBuilder
from .skill import ClawfieldSkill, SimpleRequest, GenerationResult
from .types import ProfilePicRequest, ThumbnailRequest, HeroImageRequest
from .utils import download_image, get_output_dir

__all__ = [
    # Errors
    "ClawfieldError",
    "AuthError",
    "RateLimitError",
    "InvalidModelError",
    # Core classes
    "HiggsfieldClient",
    "ClawfieldSkill",
    "BuildRequest",
    "SimpleRequest",
    "GenerationResult",
    "ProfilePicRequest",
    "ThumbnailRequest",
    "HeroImageRequest",
    # Utilities
    "download_image",
    "get_output_dir",
    "PromptBuilder",
]
