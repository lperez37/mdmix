#!/usr/bin/env python3

import os
import argparse
import glob
from datetime import datetime
import re
import sys
import time

# Color definitions for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_banner():
    """Print ASCII art banner"""
    print(f"{Colors.CYAN}")
    print("  ███╗   ███╗██████╗ ███╗   ███╗██╗██╗  ██╗")
    print("  ████╗ ████║██╔══██╗████╗ ████║██║╚██╗██╔╝")
    print("  ██╔████╔██║██║  ██║██╔████╔██║██║ ╚███╔╝ ")
    print("  ██║╚██╔╝██║██║  ██║██║╚██╔╝██║██║ ██╔██╗ ")
    print("  ██║ ╚═╝ ██║██████╔╝██║ ╚═╝ ██║██║██╔╝ ██╗")
    print("  ╚═╝     ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝")
    print(f"{Colors.NC}")
    print(f"{Colors.WHITE}{Colors.BOLD}    Markdown File Combiner{Colors.NC}")
    print(f"{Colors.PURPLE}    ═══════════════════════{Colors.NC}")
    print()

def show_progress(message, items_count=None):
    """Show progress with animation"""
    if items_count:
        print(f"{Colors.YELLOW}📊 {message} ({items_count} files){Colors.NC}")
    else:
        print(f"{Colors.YELLOW}⚙️  {message}{Colors.NC}", end="")
        for i in range(5):
            print(f"{Colors.CYAN}.{Colors.NC}", end="", flush=True)
            time.sleep(0.1)
        print(f" {Colors.GREEN}✓{Colors.NC}")

def show_success(message):
    """Show success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def show_info(message):
    """Show info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.NC}")

def show_warning(message):
    """Show warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

def show_error(message):
    """Show error message"""
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

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
    show_progress("Scanning for markdown files")
    
    pattern = os.path.join(directory, '**/*.md') if recursive else os.path.join(directory, '*.md')
    files = glob.glob(pattern, recursive=recursive)

    # Sort files by modification time (newest first)
    files.sort(key=get_file_creation_time, reverse=True)

    if not files:
        show_warning(f"No markdown files found in {directory}")
        return ""

    show_info(f"Found {len(files)} markdown file{'s' if len(files) != 1 else ''}")
    if recursive:
        show_info("Processing files recursively")
    
    print()
    show_progress("Building table of contents", len(files))

    # Generate table of contents
    toc = "# Table of Contents\n\n"
    combined_content = ""

    for i, file_path in enumerate(files, 1):
        rel_path = os.path.relpath(file_path, directory)
        title = extract_title(file_path)
        
        # Show progress for each file
        print(f"{Colors.CYAN}📄 Processing:{Colors.NC} {Colors.WHITE}{rel_path}{Colors.NC}")
        
        # Create a clean anchor ID while preserving path structure
        anchor_id = rel_path.replace('/', '-').replace(' ', '-').replace('.md', '').lower()
        
        # Add to TOC with relative path information
        toc += f"{i}. [{title}](#{anchor_id}) - `{rel_path}`\n"

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            show_error(f"Failed to read {rel_path}: {e}")
            continue

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

    print()
    show_success(f"Successfully processed {len(files)} files")
    
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
    parser.add_argument('--no-banner', action='store_true',
                       help='Skip the ASCII banner display')
    args = parser.parse_args()

    # Show banner unless disabled
    if not args.no_banner:
        print_banner()

    current_dir = os.getcwd()
    show_info(f"Working directory: {current_dir}")
    print()
    
    output_content = process_files(current_dir, args.recursive)

    if output_content:
        show_progress("Creating output file")
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(current_dir, f"mdmix-output-{timestamp}.md")

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            print()
            show_success("File creation completed!")
            print()
            print(f"{Colors.WHITE}{Colors.BOLD}Output File:{Colors.NC}")
            print(f"  {Colors.YELLOW}{output_file}{Colors.NC}")
            print()
            print(f"{Colors.GREEN}✨ Ready to use! Open the file to view your combined content{Colors.NC}")
            print()
            
        except Exception as e:
            show_error(f"Failed to write output file: {e}")
            sys.exit(1)
    else:
        show_warning("No content to write - no markdown files found")
        sys.exit(1)

if __name__ == "__main__":
    main()
