#!/usr/bin/env python3
"""Simple live generation example."""

from clawfield import ClawfieldSkill


def main():
    skill = ClawfieldSkill()
    print("Health check:", skill.health_check())

    print("\nGenerating image...")
    result = skill.generate("a friendly robot working at a desk")

    print(f"Status: {result.status}")
    print(f"URL: {result.url}")
    print(f"Saved to: {result.local_path}")

    print("\nGenerating profile pic...")
    result2 = skill.generate_profile_pic("robot manager with kind eyes")
    print(f"Saved: {result2.local_path}")


if __name__ == "__main__":
    main()
