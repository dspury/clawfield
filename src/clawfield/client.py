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
    - HF_KEY
    - HF_API_KEY
    - HF_API_SECRET
    - HF_BASE_URL (optional, defaults to API endpoint)
    """

    @staticmethod
    def _parse_credential_key(credential_key: str) -> tuple[str, str]:
        """Split a combined credential string into api key and secret."""
        api_key, separator, api_secret = credential_key.partition(":")
        if not separator or not api_key or not api_secret:
            raise AuthError(
                "HF_KEY must be formatted as '<api_key>:<api_secret>'"
            )
        return api_key, api_secret
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        credential_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.credential_key = credential_key or os.getenv("HF_KEY")
        self.api_key = api_key or os.getenv("HF_API_KEY")
        self.api_secret = api_secret or os.getenv("HF_API_SECRET")

        if self.credential_key and (not self.api_key or not self.api_secret):
            parsed_api_key, parsed_api_secret = self._parse_credential_key(self.credential_key)
            self.api_key = self.api_key or parsed_api_key
            self.api_secret = self.api_secret or parsed_api_secret

        self.base_url = base_url or os.getenv("HF_BASE_URL", "https://api.higgsfield.ai")

        if not self.api_key or not self.api_secret:
            raise AuthError(
                "HF_KEY or HF_API_KEY and HF_API_SECRET must be set via environment or arguments"
            )

        self.credential_key = f"{self.api_key}:{self.api_secret}"
    
    def _make_auth_header(self) -> str:
        """Build Authorization header."""
        return f"Key {self.credential_key}"
    
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
