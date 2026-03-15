"""Main Clawfield skill sync image generation interface."""

import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Optional, Union

from .client import HiggsfieldClient, ClawfieldError
from .builder import BuildRequest, PromptBuilder
from .utils import download_image, get_output_dir

DEFAULT_MODEL = "higgsfield-ai/soul/standard"


@dataclass
class GenerationResult:
    """Result of a successful generation."""
    url: str
    local_path: Optional[Path]
    status: str  # "completed"
    request_id: Optional[str]


@dataclass
class SimpleRequest:
    """Simple request for basic usage."""
    prompt: str
    model: str = DEFAULT_MODEL
    aspect_ratio: str = "1:1"
    resolution: str = "720p"


class ClawfieldSkill:
    """
    Sync-only skill for Higgsfield image generation.
    
    Usage:
        from clawfield import ClawfieldSkill
        
        skill = ClawfieldSkill()
        result = skill.generate("a friendly robot")
        print(result.local_path)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        output_dir: Optional[Path] = None,
    ):
        """
        Initialize skill.
        Loads credentials from args or env (HF_API_KEY, HF_API_SECRET).
        """
        # Validate credentials (raises AuthError if missing)
        self._client = HiggsfieldClient(api_key=api_key, api_secret=api_secret)
        self.output_dir = output_dir or get_output_dir()

    @staticmethod
    def _load_subscribe() -> Callable[..., object]:
        """Import the runtime generation function only when needed."""
        try:
            from higgsfield_client import subscribe
        except ImportError as exc:
            raise ClawfieldError(
                "higgsfield-client is required for image generation. "
                "Install clawfield with its runtime dependencies."
            ) from exc

        return subscribe

    @contextmanager
    def _temporary_credentials(self) -> Iterator[None]:
        """
        Expose explicit credentials to the downstream client for one call.

        The upstream dependency reads `HF_API_KEY` and `HF_API_SECRET` from the
        environment, so constructor-provided credentials must be mirrored there
        while generation is in progress.
        """
        old_api_key = os.environ.get("HF_API_KEY")
        old_api_secret = os.environ.get("HF_API_SECRET")

        os.environ["HF_API_KEY"] = self._client.api_key
        os.environ["HF_API_SECRET"] = self._client.api_secret
        try:
            yield
        finally:
            if old_api_key is None:
                os.environ.pop("HF_API_KEY", None)
            else:
                os.environ["HF_API_KEY"] = old_api_key

            if old_api_secret is None:
                os.environ.pop("HF_API_SECRET", None)
            else:
                os.environ["HF_API_SECRET"] = old_api_secret

    @staticmethod
    def _extract_image_url(result: object) -> tuple[str, Optional[str]]:
        """Normalize the upstream response into the image URL and request id."""
        if isinstance(result, dict):
            request_id = result.get("request_id")
            images = result.get("images") or result.get("outputs") or []
            if not images:
                raise ClawfieldError("No images in response")

            first_image = images[0]
            if isinstance(first_image, dict):
                image_url = first_image.get("url")
                if not image_url:
                    raise ClawfieldError("Image response missing url")
                return image_url, request_id

            return str(first_image), request_id

        return str(result), None
    
    def generate(
        self,
        request: Union[str, SimpleRequest, BuildRequest],
        filename: Optional[str] = None,
        download: bool = True,
    ) -> GenerationResult:
        """
        Generate image — sync, blocking, polls until complete.
        
        Args:
            request: String prompt, SimpleRequest, or BuildRequest
            filename: Custom filename (optional)
            download: If True, download image to local path
        
        Returns:
            GenerationResult with url, local_path, status, request_id
        
        Raises:
            ClawfieldError: On auth, rate limit, or generation failure
        """
        # Convert request to API arguments
        model = DEFAULT_MODEL
        if isinstance(request, str):
            args = {
                "prompt": request,
                "aspect_ratio": "1:1",
                "resolution": "720p",
            }
        elif isinstance(request, SimpleRequest):
            model = request.model
            args = {
                "prompt": request.prompt,
                "aspect_ratio": request.aspect_ratio,
                "resolution": request.resolution,
            }
        elif isinstance(request, BuildRequest):
            args = {
                "prompt": request.to_prompt(),
                "aspect_ratio": "1:1",  # BuildRequest defaults to this
                "resolution": "720p",
            }
        else:
            raise ClawfieldError(f"Unknown request type: {type(request)}")
        
        subscribe = self._load_subscribe()

        # Call Higgsfield (blocking, polls internally via subscribe())
        try:
            with self._temporary_credentials():
                result = subscribe(model, arguments=args)
        except ClawfieldError:
            raise
        except Exception as e:
            # Map to clean error
            error_msg = str(e).lower()
            if "401" in error_msg or "403" in error_msg:
                from .client import AuthError
                raise AuthError(f"Authentication failed: check HF_API_KEY and HF_API_SECRET")
            elif "429" in error_msg:
                from .client import RateLimitError
                raise RateLimitError(f"Rate limited: {e}")
            elif "422" in error_msg:
                from .client import InvalidModelError
                raise InvalidModelError(f"Invalid request: {e}")
            raise ClawfieldError(f"Generation failed: {e}")
        
        image_url, request_id = self._extract_image_url(result)
        
        # Download if requested
        local_path = None
        if download:
            local_path = download_image(image_url, self.output_dir, filename)
        
        return GenerationResult(
            url=image_url,
            local_path=local_path,
            status="completed",
            request_id=request_id,
        )
    
    def generate_profile_pic(
        self,
        subject: str,
        style: str = "professional",
        filename: Optional[str] = None,
    ) -> GenerationResult:
        """Convenience: profile picture generation."""
        prompt = PromptBuilder.profile_pic(subject, mood=style)
        return self.generate(prompt, filename=filename)
    
    def generate_thumbnail(
        self,
        scene: str,
        subject: str,
        contrast: str = "high",
    ) -> GenerationResult:
        """Convenience: thumbnail generation."""
        prompt = PromptBuilder.thumbnail(scene, subject, contrast=contrast)
        return self.generate(prompt)
    
    def health_check(self) -> dict:
        """Check if skill is properly configured."""
        return self._client.health_check()
