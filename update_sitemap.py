#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Script to automatically create/update sitemap.md with links to all markdown files in the blog folder.

Note that this script is run by a git hook on pre-commit.
"""

import re
import subprocess
from pathlib import Path


def delinkify(text):
    """
    Remove markdown link syntax, keeping only the link text.
    Converts [text](url) to just text.
    """
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def get_markdown_title(filepath):
    """
    Extract the title from a markdown file (first line starting with single #).
    Raises an error if no title is found.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Skip empty lines and HTML comments
            stripped = line.strip()
            if not stripped or stripped.startswith("<!--"):
                continue
            # Check for single # (not ## or more)
            match = re.match(r"^#\s+(.+)$", stripped)
            if match:
                title = match.group(1).strip()
                # Remove any markdown links from the title
                return delinkify(title)
            # If we hit a non-empty, non-comment line that's not a title, keep looking
            # (in case there's frontmatter or other content before the title)

    raise ValueError(f"No markdown title (# Title) found in {filepath}")


def filter_gitignored(directory, paths):
    """Drop paths that git would ignore. Falls back to no filtering if git is unavailable."""
    if not paths:
        return paths
    str_paths = [str(p) for p in paths]
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            input="\n".join(str_paths),
            capture_output=True,
            text=True,
            cwd=directory,
        )
    except (FileNotFoundError, OSError):
        return paths
    # 0 = some ignored, 1 = none ignored; anything else is an error.
    if result.returncode not in (0, 1):
        return paths
    ignored = set(result.stdout.splitlines())
    return [p for p, s in zip(paths, str_paths) if s not in ignored]


def get_markdown_files(directory):
    """Get all markdown files in the directory, excluding gitignored paths."""
    root_matches = sorted(Path(directory).glob("*.md"))
    root_matches = filter_gitignored(directory, root_matches)
    md_files = [f.name for f in root_matches]

    nested_matches = sorted(Path(directory).glob("*/*.md"))
    nested_matches = filter_gitignored(directory, nested_matches)
    subdirs = {}
    for file in nested_matches:
        subdir = file.parent.name
        subdirs.setdefault(subdir, []).append(file.relative_to(directory))

    return md_files, subdirs


def create_sitemap_content(directory, md_files, subdirs):
    """Create the full sitemap content with links to all blog posts."""
    lines = ["# Blog Sitemap\n\n"]
    lines.append(
        "This is an automatically generated sitemap of all blog posts in this repository.\n\n"
    )

    if md_files:
        lines.append("- **Main Posts**\n")
        for filename in md_files:
            filepath = Path(directory) / filename
            title = get_markdown_title(filepath)
            lines.append(f"  - [{title}]({filename})\n")

    if subdirs:
        for subdir, files in sorted(subdirs.items()):
            lines.append(
                f"- **{subdir.replace('-', ' ').replace('_', ' ').title()}**\n"
            )
            for filepath in files:
                full_path = Path(directory) / filepath
                title = get_markdown_title(full_path)
                lines.append(f"  - [{title}]({filepath})\n")

    return "".join(lines)


def update_sitemap(directory):
    """Create or update the sitemap.md file with links to all markdown files."""
    sitemap_path = Path(directory) / "sitemap.md"

    # Get markdown files
    md_files, subdirs = get_markdown_files(directory)

    # Create sitemap content
    sitemap_content = create_sitemap_content(directory, md_files, subdirs)

    # Write sitemap file
    with open(sitemap_path, "w") as f:
        f.write(sitemap_content)

    print("✅ ./sitemap.md created/updated successfully!")
    print(f"📝 Found {len(md_files)} markdown files in root directory")
    if subdirs:
        total_subdir_files = sum(len(files) for files in subdirs.values())
        print(
            f"📁 Found {total_subdir_files} markdown files in {len(subdirs)} subdirectories"
        )


if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    update_sitemap(script_dir)
