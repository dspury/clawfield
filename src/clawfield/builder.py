"""Structured prompt builder for Higgsfield generation."""

from dataclasses import dataclass
from typing import Optional


# Generic composition presets (not brand-specific)
COMPOSITION_PRESETS = {
    "wide": "wide angle shot, environment visible, establishing composition",
    "medium": "waist up framing, clear subject, contextual background",
    "close": "close-up detail, sharp focus, textural emphasis",
    "centered": "centered subject, clear silhouette, minimal distractions",
}

# Generic lighting presets (not tentpole-specific)
LIGHTING_PRESETS = {
    "natural": "natural daylight, soft and even",
    "golden": "golden hour warmth, gentle backlight",
    "dramatic": "dramatic side lighting, high contrast",
    "studio": "soft studio lighting, clean and professional",
}


@dataclass
class BuildRequest:
    """
    Structured request for image generation.
    Generic - no brand-specific fields.
    """
    scene: str
    subject: str
    composition: str = "medium"  # key from COMPOSITION_PRESETS
    environment: str = ""
    lighting: str = "natural"  # key from LIGHTING_PRESETS
    quality: str = "high detail"
    
    def __post_init__(self):
        # Resolve composition preset
        if self.composition in COMPOSITION_PRESETS:
            self._composition_text = COMPOSITION_PRESETS[self.composition]
        else:
            self._composition_text = self.composition
        
        # Resolve lighting preset
        if self.lighting in LIGHTING_PRESETS:
            self._lighting_text = LIGHTING_PRESETS[self.lighting]
        else:
            self._lighting_text = self.lighting
    
    def to_prompt(self) -> str:
        """Build structured prompt per Higgsfield spec."""
        parts = [
            self.scene,
            f"subject: {self.subject}",
            f"composition: {self._composition_text}",
        ]
        
        if self.environment:
            parts.append(f"environment: {self.environment}")
        
        parts.append(f"lighting: {self._lighting_text}")
        parts.append(f"quality: {self.quality}")
        
        return "\n\n".join(parts)


def lint_prompt(prompt: str) -> str:
    """
    Clean prompt of Higgsfield-degrading terms.
    Returns cleaned prompt.
    """
    forbidden = [
        "masterpiece", "trending on artstation", "best quality",
        "8k", "award winning", "ultra detailed", "insane detail"
    ]
    
    cleaned = prompt.lower()
    for term in forbidden:
        cleaned = cleaned.replace(term, "")
    
    # Restore original casing by reconstructing
    return prompt  # Phase 2: basic pass, linting in Phase 3


class PromptBuilder:
    """High-level builder for common image types."""
    
    @staticmethod
    def profile_pic(subject: str, environment: str = "", mood: str = "professional") -> str:
        """Build professional portrait prompt."""
        request = BuildRequest(
            scene=f"Professional portrait of {subject}",
            subject=subject,
            composition="medium",
            environment=environment or "clean minimal background",
            lighting="studio" if mood == "professional" else "natural",
        )
        return request.to_prompt()
    
    @staticmethod
    def thumbnail(scene: str, subject: str, contrast: str = "high") -> str:
        """Build thumbnail-optimized prompt."""
        lighting = "dramatic" if contrast == "high" else "natural"
        request = BuildRequest(
            scene=scene,
            subject=subject,
            composition="centered",
            lighting=lighting,
        )
        return request.to_prompt()
    
    @staticmethod
    def hero_image(scene: str, subject: str, environment: str) -> str:
        """Build wide establishing shot."""
        request = BuildRequest(
            scene=scene,
            subject=subject,
            composition="wide",
            environment=environment,
            lighting="golden",
        )
        return request.to_prompt()
