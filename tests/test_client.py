"""Tests for clawfield client (mocked, no live API)."""

import os
import pytest
from clawfield.client import HiggsfieldClient, AuthError


class TestAuth:
    """Authentication loading tests."""
    
    def test_raises_without_credentials(self):
        """Should raise AuthError when no creds provided."""
        # Ensure env is clean
        for key in ["HF_API_KEY", "HF_API_SECRET"]:
            os.environ.pop(key, None)
        
        with pytest.raises(AuthError) as exc_info:
            HiggsfieldClient()
        
        assert "HF_API_KEY" in str(exc_info.value)
    
    def test_accepts_explicit_credentials(self):
        """Should accept credentials via constructor."""
        client = HiggsfieldClient(
            api_key="test-key-123",
            api_secret="test-secret-456",
        )
        
        assert client.api_key == "test-key-123"
        assert client.api_secret == "test-secret-456"
    
    def test_loads_from_environment(self, monkeypatch):
        """Should load credentials from environment variables."""
        monkeypatch.setenv("HF_API_KEY", "env-key-789")
        monkeypatch.setenv("HF_API_SECRET", "env-secret-abc")
        
        client = HiggsfieldClient()
        
        assert client.api_key == "env-key-789"
        assert client.api_secret == "env-secret-abc"
    
    def test_explicit_overrides_environment(self, monkeypatch):
        """Constructor args should override environment."""
        monkeypatch.setenv("HF_API_KEY", "env-key")
        monkeypatch.setenv("HF_API_SECRET", "env-secret")
        
        client = HiggsfieldClient(
            api_key="explicit-key",
            api_secret="explicit-secret",
        )
        
        assert client.api_key == "explicit-key"


class TestHealthCheck:
    """Basic connectivity tests (no live calls)."""
    
    def test_returns_status_dict(self):
        """Health check should return metadata without API call."""
        client = HiggsfieldClient(api_key="test", api_secret="test")
        result = client.health_check()
        
        assert result["status"] == "ok"
        assert result["client"] == "clawfield"
        assert result["auth_configured"] is True
    
    def test_auth_configured_false_when_empty(self):
        """Edge case: empty strings should report as not configured."""
        # This requires explicit empty strings (not None)
        client = HiggsfieldClient(api_key="test", api_secret="test")
        # Force empty via attribute manipulation for edge case test
        client.api_key = ""
        result = client.health_check()
        
        assert result["auth_configured"] is False
