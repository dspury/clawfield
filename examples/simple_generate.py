#!/usr/bin/env python3
"""Example: Simple tier-1 usage."""

from clawfield import ClawfieldSkill

# Requires HF_API_KEY and HF_API_SECRET in environment
def main():
    skill = ClawfieldSkill()
    print("Health check:", skill.health_check())
    
    # Simple string prompt
    print("\nGenerating image...")
    result = skill.generate("a friendly robot working at a desk")
    
    print(f"Status: {result.status}")
    print(f"URL: {result.url}")
    print(f"Saved to: {result.local_path}")
    
    # Profile pic convenience
    print("\nGenerating profile pic...")
    result2 = skill.generate_profile_pic("robot manager with kind eyes")
    print(f"Saved: {result2.local_path}")

if __name__ == "__main__":
    main()
