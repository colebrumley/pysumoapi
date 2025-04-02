#!/usr/bin/env python3
"""
Version management script for PySumoAPI.
"""

import argparse
import re
import sys
from pathlib import Path


def read_version(file_path: str) -> str:
    """Read version from pyproject.toml."""
    with open(file_path, "r") as f:
        content = f.read()
    
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError(f"Could not find version in {file_path}")
    
    return match.group(1)


def update_version(file_path: str, new_version: str) -> None:
    """Update version in pyproject.toml."""
    with open(file_path, "r") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'(version\s*=\s*)"([^"]+)"',
        f'\\1"{new_version}"',
        content
    )
    
    with open(file_path, "w") as f:
        f.write(updated_content)


def update_changelog(changelog_path: str, new_version: str) -> None:
    """Update CHANGELOG.md with a new version entry."""
    with open(changelog_path, "r") as f:
        content = f.read()
    
    # Check if the version already exists
    if f"## [{new_version}]" in content:
        print(f"Warning: Version {new_version} already exists in CHANGELOG.md")
        return
    
    # Add new version entry after the first heading
    updated_content = re.sub(
        r'(# Changelog\n\n)',
        f'\\1## [{new_version}] - {get_current_date()}\n\n### Added\n- \n\n',
        content
    )
    
    with open(changelog_path, "w") as f:
        f.write(updated_content)


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump version according to semantic versioning."""
    major, minor, patch = map(int, current_version.split("."))
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Version management for PySumoAPI")
    parser.add_argument(
        "action",
        choices=["show", "bump", "set"],
        help="Action to perform"
    )
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch"],
        help="Bump type (for 'bump' action)"
    )
    parser.add_argument(
        "--version",
        help="New version (for 'set' action)"
    )
    
    args = parser.parse_args()
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"
    changelog_path = project_root / "CHANGELOG.md"
    
    # Read current version
    current_version = read_version(pyproject_path)
    
    if args.action == "show":
        print(f"Current version: {current_version}")
    
    elif args.action == "bump":
        if not args.type:
            parser.error("--type is required for 'bump' action")
        
        new_version = bump_version(current_version, args.type)
        print(f"Bumping version from {current_version} to {new_version}")
        
        update_version(pyproject_path, new_version)
        update_changelog(changelog_path, new_version)
        
        print(f"Version updated to {new_version}")
        print(f"Don't forget to commit the changes and create a tag: git tag v{new_version}")
    
    elif args.action == "set":
        if not args.version:
            parser.error("--version is required for 'set' action")
        
        # Validate version format
        if not re.match(r'^\d+\.\d+\.\d+$', args.version):
            print("Error: Version must be in the format X.Y.Z")
            sys.exit(1)
        
        print(f"Setting version from {current_version} to {args.version}")
        
        update_version(pyproject_path, args.version)
        update_changelog(changelog_path, args.version)
        
        print(f"Version updated to {args.version}")
        print(f"Don't forget to commit the changes and create a tag: git tag v{args.version}")


if __name__ == "__main__":
    main() 