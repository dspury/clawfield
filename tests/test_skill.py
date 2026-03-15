"""Tests for the Clawfield skill surface."""

from pathlib import Path

import pytest

from clawfield import ClawfieldError, ClawfieldSkill, GenerationResult, SimpleRequest


class TestSkillImports:
    """Import and dependency handling tests."""

    def test_dependency_errors_surface_without_generic_wrapping(self, monkeypatch, tmp_path):
        """Dependency failures should remain first-class Clawfield errors."""
        skill = ClawfieldSkill(api_key="test-key", api_secret="test-secret", output_dir=tmp_path)

        monkeypatch.setattr(
            ClawfieldSkill,
            "_load_subscribe",
            staticmethod(lambda: (_ for _ in ()).throw(ClawfieldError("higgsfield-client is required"))),
        )

        with pytest.raises(ClawfieldError) as exc_info:
            skill.generate("test prompt")

        assert "higgsfield-client" in str(exc_info.value)


class TestSkillGeneration:
    """Generation request and response handling tests."""

    def test_simple_request_uses_requested_model(self, monkeypatch, tmp_path):
        """SimpleRequest.model should be forwarded to the runtime client."""
        skill = ClawfieldSkill(api_key="test-key", api_secret="test-secret", output_dir=tmp_path)
        called = {}

        def fake_subscribe(model, arguments):
            called["model"] = model
            called["arguments"] = arguments
            return {"request_id": "req-123", "images": [{"url": "https://example.com/image.png"}]}

        monkeypatch.setattr(ClawfieldSkill, "_load_subscribe", staticmethod(lambda: fake_subscribe))
        monkeypatch.setattr("clawfield.skill.download_image", lambda *args, **kwargs: tmp_path / "image.png")

        result = skill.generate(
            SimpleRequest(
                prompt="test prompt",
                model="custom/model",
                aspect_ratio="16:9",
                resolution="1080p",
            )
        )

        assert called["model"] == "custom/model"
        assert called["arguments"] == {
            "prompt": "test prompt",
            "aspect_ratio": "16:9",
            "resolution": "1080p",
        }
        assert result == GenerationResult(
            url="https://example.com/image.png",
            local_path=tmp_path / "image.png",
            status="completed",
            request_id="req-123",
        )

    def test_generate_without_download_returns_none_local_path(self, monkeypatch, tmp_path):
        """Skipping the download should leave `local_path` unset."""
        skill = ClawfieldSkill(api_key="test-key", api_secret="test-secret", output_dir=tmp_path)

        monkeypatch.setattr(
            ClawfieldSkill,
            "_load_subscribe",
            staticmethod(lambda: lambda model, arguments: {"images": [{"url": "https://example.com/image.png"}]}),
        )

        result = skill.generate("test prompt", download=False)

        assert result.local_path is None
        assert result.url == "https://example.com/image.png"

    def test_generate_restores_environment_credentials(self, monkeypatch, tmp_path):
        """Temporary credentials should not leak after generation completes."""
        skill = ClawfieldSkill(
            api_key="explicit-key",
            api_secret="explicit-secret",
            output_dir=tmp_path,
        )
        monkeypatch.setenv("HF_KEY", "original-key:original-secret")
        monkeypatch.setenv("HF_API_KEY", "original-key")
        monkeypatch.setenv("HF_API_SECRET", "original-secret")

        captured = {}

        def fake_subscribe(model, arguments):
            import os

            captured["credential_key"] = os.environ.get("HF_KEY")
            captured["api_key"] = os.environ.get("HF_API_KEY")
            captured["api_secret"] = os.environ.get("HF_API_SECRET")
            return {"images": [{"url": "https://example.com/image.png"}]}

        monkeypatch.setattr(ClawfieldSkill, "_load_subscribe", staticmethod(lambda: fake_subscribe))
        monkeypatch.setattr("clawfield.skill.download_image", lambda *args, **kwargs: Path(tmp_path / "image.png"))

        skill.generate("test prompt")

        assert captured == {
            "credential_key": "explicit-key:explicit-secret",
            "api_key": "explicit-key",
            "api_secret": "explicit-secret",
        }
        assert __import__("os").environ["HF_KEY"] == "original-key:original-secret"
        assert __import__("os").environ["HF_API_KEY"] == "original-key"
        assert __import__("os").environ["HF_API_SECRET"] == "original-secret"

    def test_generate_with_explicit_credential_key(self, monkeypatch, tmp_path):
        """Combined credentials should work through the skill surface."""
        skill = ClawfieldSkill(
            credential_key="combined-key:combined-secret",
            output_dir=tmp_path,
        )
        captured = {}

        def fake_subscribe(model, arguments):
            import os

            captured["credential_key"] = os.environ.get("HF_KEY")
            captured["api_key"] = os.environ.get("HF_API_KEY")
            captured["api_secret"] = os.environ.get("HF_API_SECRET")
            return {"images": [{"url": "https://example.com/image.png"}]}

        monkeypatch.setattr(ClawfieldSkill, "_load_subscribe", staticmethod(lambda: fake_subscribe))
        monkeypatch.setattr("clawfield.skill.download_image", lambda *args, **kwargs: Path(tmp_path / "image.png"))

        skill.generate("test prompt")

        assert captured == {
            "credential_key": "combined-key:combined-secret",
            "api_key": "combined-key",
            "api_secret": "combined-secret",
        }
