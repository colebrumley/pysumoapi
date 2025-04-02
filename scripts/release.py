#!/usr/bin/env python3
"""
Release script for PySumoAPI.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    try:
        return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")
        sys.exit(1)


def check_git_clean() -> None:
    """Check if git working directory is clean."""
    result = run_command(["git", "status", "--porcelain"])
    if result.stdout.strip():
        print("Error: Git working directory is not clean.")
        print("Please commit or stash your changes before releasing.")
        sys.exit(1)


def check_git_branch() -> None:
    """Check if we're on the main branch."""
    result = run_command(["git", "branch", "--show-current"])
    if result.stdout.strip() != "main":
        print("Error: Not on main branch.")
        print("Please switch to the main branch before releasing.")
        sys.exit(1)


def check_git_remote() -> None:
    """Check if local is up to date with remote."""
    run_command(["git", "fetch", "origin", "main"])
    result = run_command(["git", "rev-list", "HEAD..origin/main", "--count"])
    if int(result.stdout.strip()) != 0:
        print("Error: Local branch is behind remote.")
        print("Please pull the latest changes before releasing.")
        sys.exit(1)


def check_dependencies() -> None:
    """Check if all required tools are installed."""
    tools = ["git", "uv", "python"]
    for tool in tools:
        try:
            run_command([tool, "--version"])
        except FileNotFoundError:
            print(f"Error: {tool} is not installed.")
            sys.exit(1)


def check_pypi_token() -> None:
    """Check if PYPI_API_TOKEN is set."""
    if "PYPI_API_TOKEN" not in os.environ:
        print("Warning: PYPI_API_TOKEN environment variable is not set.")
        print("Package will not be published to PyPI.")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create a new release for PySumoAPI")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests"
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip running linters"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip building the package"
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Skip publishing to PyPI"
    )
    parser.add_argument(
        "--skip-tag",
        action="store_true",
        help="Skip creating a git tag"
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip pre-release checks"
    )
    
    args = parser.parse_args()
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    # Pre-release checks
    if not args.skip_checks:
        print("Running pre-release checks...")
        check_dependencies()
        check_git_clean()
        check_git_branch()
        check_git_remote()
        if not args.skip_publish:
            check_pypi_token()
    
    # Step 1: Bump version
    print("Bumping version...")
    run_command(["make", "version-bump", f"TYPE={args.bump_type}"], cwd=project_root)
    
    # Get the new version
    result = run_command(["make", "version"], cwd=project_root)
    new_version = result.stdout.strip().split(": ")[1]
    
    # Step 2: Run tests
    if not args.skip_tests:
        print("Running tests...")
        run_command(["make", "test"], cwd=project_root)
    
    # Step 3: Run linters
    if not args.skip_lint:
        print("Running linters...")
        run_command(["make", "lint"], cwd=project_root)
    
    # Step 4: Build the package
    if not args.skip_build:
        print("Building package...")
        run_command(["make", "build"], cwd=project_root)
    
    # Step 5: Publish to PyPI
    if not args.skip_publish:
        print("Publishing to PyPI...")
        if "PYPI_API_TOKEN" not in os.environ:
            print("Error: PYPI_API_TOKEN environment variable is not set")
            print("Skipping publish step")
        else:
            run_command(["make", "publish"], cwd=project_root)
    
    # Step 6: Create git tag
    if not args.skip_tag:
        print("Creating git tag...")
        tag_name = f"v{new_version}"
        run_command(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], cwd=project_root)
        print(f"Created tag {tag_name}")
        print(f"Don't forget to push the tag: git push origin {tag_name}")
    
    print("\nRelease completed successfully!")
    print(f"Version: {new_version}")
    print("\nNext steps:")
    print(f"1. Commit your changes: git commit -am 'Release {new_version}'")
    print("2. Push your changes: git push origin main")
    if not args.skip_tag:
        print(f"3. Push the tag: git push origin v{new_version}")


if __name__ == "__main__":
    main() 