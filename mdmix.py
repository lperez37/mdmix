#!/usr/bin/env python3

import os
import argparse
import glob
from datetime import datetime
import re

def get_file_creation_time(file_path):
    """Get file creation time for sorting"""
    return os.path.getmtime(file_path)

def extract_title(file_path):
    """Extract title from markdown file (first # heading)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1)
            else:
                return os.path.basename(file_path)
    except:
        return os.path.basename(file_path)

def process_files(directory, recursive=False):
    """Process markdown files and return combined content with TOC"""
    pattern = os.path.join(directory, '**/*.md') if recursive else os.path.join(directory, '*.md')
    files = glob.glob(pattern, recursive=recursive)

    # Sort files by modification time (newest first)
    files.sort(key=get_file_creation_time, reverse=True)

    if not files:
        print(f"No markdown files found in {directory}")
        return ""

    # Generate table of contents
    toc = "# Table of Contents\n\n"
    combined_content = ""

    for i, file_path in enumerate(files, 1):
        rel_path = os.path.relpath(file_path, directory)
        title = extract_title(file_path)
        
        # Create a clean anchor ID while preserving path structure
        anchor_id = rel_path.replace('/', '-').replace(' ', '-').replace('.md', '').lower()
        
        # Add to TOC with relative path information
        toc += f"{i}. [{title}](#{anchor_id}) - `{rel_path}`\n"

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add file to combined content with document tags
        combined_content += f"\n\n<document id=\"{anchor_id}\" source=\"{rel_path}\">\n"
        combined_content += f"## File: {rel_path}\n\n"

        # Add folder tags if in subdirectory (always show folder info for clarity)
        if os.path.dirname(rel_path):
            folder_path = os.path.dirname(rel_path)
            combined_content += f"<folder>{folder_path}</folder>\n"
            combined_content += f"**Directory:** `{folder_path}`\n"
            combined_content += f"**Full Path:** `{rel_path}`\n\n"
        else:
            combined_content += f"**Directory:** `./` (root)\n"
            combined_content += f"**Full Path:** `{rel_path}`\n\n"

        combined_content += content
        combined_content += "\n</document>\n"

    # Combine TOC and content
    return toc + combined_content

def main():
    parser = argparse.ArgumentParser(
        description='Combine markdown files with table of contents',
        epilog='Examples:\n'
               '  mdmix           # Combine .md files in current directory\n'
               '  mdmix -r        # Combine .md files recursively\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process subdirectories recursively')
    args = parser.parse_args()

    current_dir = os.getcwd()
    output_content = process_files(current_dir, args.recursive)

    if output_content:
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(current_dir, f"mdmix-output-{timestamp}.md")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Combined markdown file created: {output_file}")

if __name__ == "__main__":
    main()
