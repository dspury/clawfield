"""Thin client wrapper for Higgsfield API with retry logic."""

import os
from typing import Optional


class ClawfieldError(Exception):
    """Base error for clawfield skill."""
    pass


class AuthError(ClawfieldError):
    """Authentication failed (401/403)."""
    pass


class RateLimitError(ClawfieldError):
    """Rate limit hit (429)."""
    pass


class InvalidModelError(ClawfieldError):
    """Model not found or invalid (404/422)."""
    pass


class HiggsfieldClient:
    """
    Minimal client for Higgsfield API.
    
    Loads auth from environment:
    - HF_API_KEY
    - HF_API_SECRET
    - HF_BASE_URL (optional, defaults to API endpoint)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HF_API_KEY")
        self.api_secret = api_secret or os.getenv("HF_API_SECRET")
        self.base_url = base_url or os.getenv("HF_BASE_URL", "https://api.higgsfield.ai")
        
        if not self.api_key or not self.api_secret:
            raise AuthError(
                "HF_API_KEY and HF_API_SECRET must be set via environment or arguments"
            )
    
    def _make_auth_header(self) -> str:
        """Build Authorization header."""
        return f"Key {self.api_key}:{self.api_secret}"
    
    def health_check(self) -> dict:
        """
        Test connectivity and auth.
        Returns status dict without burning credits.
        """
        # Phase 1: placeholder - actual implementation in Phase 3
        return {
            "status": "ok",
            "client": "clawfield",
            "version": "0.1.0",
            "auth_configured": bool(self.api_key and self.api_secret),
        }
