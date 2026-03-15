"""Tests for prompt builder (no API calls)."""

from clawfield.builder import BuildRequest, PromptBuilder, COMPOSITION_PRESETS, LIGHTING_PRESETS


class TestBuildRequest:
    """Structured prompt construction tests."""
    
    def test_basic_structure(self):
        """Should build 5-part structure."""
        request = BuildRequest(
            scene="Robot at command center",
            subject="sleek android with glowing eyes",
            environment="high-tech control room",
            composition="medium",
            lighting="dramatic",
        )
        
        prompt = request.to_prompt()
        
        assert "Robot at command center" in prompt
        assert "subject: sleek android with glowing eyes" in prompt
        assert "composition:" in prompt
        assert "environment: high-tech control room" in prompt
        assert "lighting:" in prompt
        assert "quality: high detail" in prompt
        print("✅ Test: Basic structure correct")
    
    def test_composition_preset_resolution(self):
        """Should resolve 'medium' to preset text."""
        request = BuildRequest(
            scene="Test scene",
            subject="Test subject",
            composition="wide"
        )
        
        assert request._composition_text == COMPOSITION_PRESETS["wide"]
        print("✅ Test: Composition preset resolved")
    
    def test_lighting_preset_resolution(self):
        """Should resolve 'golden' to preset text."""
        request = BuildRequest(
            scene="Test scene",
            subject="Test subject",
            lighting="golden"
        )
        
        assert request._lighting_text == LIGHTING_PRESETS["golden"]
        print("✅ Test: Lighting preset resolved")
    
    def test_custom_composition_fallback(self):
        """Should accept custom composition if not in presets."""
        custom = "custom framing description"
        request = BuildRequest(
            scene="Test scene",
            subject="Test subject",
            composition=custom
        )
        
        assert request._composition_text == custom
        print("✅ Test: Custom composition accepted")


class TestPromptBuilder:
    """Convenience builder tests."""
    
    def test_profile_pic(self):
        """Should build professional portrait."""
        prompt = PromptBuilder.profile_pic(
            subject="friendly robot manager",
            environment="clean office background"
        )
        
        assert "Professional portrait" in prompt
        assert "subject: friendly robot manager" in prompt
        assert "composition:" in prompt
        assert "studio" in prompt.lower() or "professional" in prompt.lower()
        print("✅ Test: Profile pic builder works")
    
    def test_thumbnail(self):
        """Should build thumbnail with centered composition."""
        prompt = PromptBuilder.thumbnail(
            scene="Surprising discovery",
            subject="reactor core glowing",
            contrast="high"
        )
        
        assert "Surprising discovery" in prompt
        assert "subject: reactor core glowing" in prompt
        assert "centered" in prompt.lower() or "center" in prompt.lower()
        print("✅ Test: Thumbnail builder works")
    
    def test_hero_image(self):
        """Should build wide establishing shot."""
        prompt = PromptBuilder.hero_image(
            scene="Teens enter facility",
            subject="group of curious teenagers",
            environment="massive industrial entrance"
        )
        
        assert "Teens enter facility" in prompt
        assert "wide" in prompt.lower() or "wide angle" in prompt.lower()
        assert "massive industrial entrance" in prompt
        print("✅ Test: Hero image builder works")


def run_all_tests():
    """Manual test runner (no pytest dependency)."""
    print("\n🧪 Phase 2: Builder Tests")
    print("=" * 50)
    
    test_classes = [TestBuildRequest, TestPromptBuilder]
    
    for cls in test_classes:
        print(f"\nTesting {cls.__name__}...")
        instance = cls()
        for attr in dir(instance):
            if attr.startswith("test_"):
                try:
                    getattr(instance, attr)()
                except AssertionError as e:
                    print(f"  ❌ FAILED: {attr} - {e}")
                except Exception as e:
                    print(f"  ❌ ERROR: {attr} - {e}")
    
    print("\n" + "=" * 50)
    print("✅ Phase 2 complete")


if __name__ == "__main__":
    run_all_tests()
