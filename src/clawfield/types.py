"""Pre-built convenience types for common generation patterns."""

from dataclasses import dataclass
from typing import Optional

from .builder import BuildRequest


@dataclass
class ProfilePicRequest:
    """
    Request for professional portrait-style image.
    
    Example:
        ProfilePicRequest(
            subject="friendly robot",
            environment="clean office",
            mood="professional"
        )
    """
    subject: str
    environment: str = "clean minimal background"
    mood: str = "professional"  # or "casual", "dramatic"
    
    def to_build_request(self) -> BuildRequest:
        """Convert to base BuildRequest."""
        lighting = {
            "professional": "studio",
            "casual": "natural",
            "dramatic": "dramatic"
        }.get(self.mood, "studio")
        
        return BuildRequest(
            scene=f"Professional portrait of {self.subject}",
            subject=self.subject,
            composition="medium",
            environment=self.environment,
            lighting=lighting,
        )


@dataclass
class ThumbnailRequest:
    """
    Request for thumbnail-optimized image.
    High contrast, centered, eye-catching.
    
    Example:
        ThumbnailRequest(
            scene="surprising discovery",
            subject="reactor core",
            contrast="high"
        )
    """
    scene: str
    subject: str
    contrast: str = "high"  # or "low"
    
    def to_build_request(self) -> BuildRequest:
        """Convert to base BuildRequest."""
        lighting = "dramatic" if self.contrast == "high" else "natural"
        
        return BuildRequest(
            scene=self.scene,
            subject=self.subject,
            composition="centered",
            environment="minimal background",
            lighting=lighting,
        )


@dataclass
class HeroImageRequest:
    """
    Request for wide establishing shot.
    Used for headers, hero sections, full-width images.
    
    Example:
        HeroImageRequest(
            scene="teens enter facility",
            subject="group of teenagers",
            environment="massive industrial doorway"
        )
    """
    scene: str
    subject: str
    environment: str
    time_of_day: str = "golden"  # or "day", "night"
    
    def to_build_request(self) -> BuildRequest:
        """Convert to base BuildRequest."""
        lighting = {
            "golden": "golden",
            "day": "natural",
            "night": "dramatic"
        }.get(self.time_of_day, "golden")
        
        return BuildRequest(
            scene=self.scene,
            subject=self.subject,
            composition="wide",
            environment=self.environment,
            lighting=lighting,
        )
