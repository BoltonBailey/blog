#!/usr/bin/env python3
"""
Script to automatically create/update sitemap.md with links to all markdown files in the blog folder.
"""

import re
from pathlib import Path


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
                return match.group(1).strip()
            # If we hit a non-empty, non-comment line that's not a title, keep looking
            # (in case there's frontmatter or other content before the title)

    raise ValueError(f"No markdown title (# Title) found in {filepath}")


def get_markdown_files(directory):
    """Get all markdown files in the directory."""
    md_files = []

    # Get all .md files in the root directory
    for file in sorted(Path(directory).glob("*.md")):
        md_files.append(file.name)

    # Get all .md files in subdirectories
    subdirs = {}
    for file in sorted(Path(directory).glob("*/*.md")):
        subdir = file.parent.name
        if subdir not in subdirs:
            subdirs[subdir] = []
        subdirs[subdir].append(file.relative_to(directory))

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

    print("✅ sitemap.md created/updated successfully!")
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
