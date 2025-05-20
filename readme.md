# MDMix - Markdown File Combiner

A Python utility that combines multiple Markdown files into a single document with an automatically generated table of contents.

## Features

- Combines all `.md` files in the current directory into a single document
- Creates a comprehensive table of contents with links to each section
- Orders files from newest to oldest based on modification time
- Clearly separates documents with custom tags
- Supports recursive directory processing
- Generates timestamped output files
- Extracts titles from headings for better organization

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mdmix.git
   cd mdmix
   ```

2. Make the script executable:
   ```bash
   chmod +x mdmix
   ```

3. Add to your PATH (optional):
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$PATH:/path/to/mdmix"
   ```

## Usage

### Basic Usage

Run in any directory containing Markdown files:

```bash
mdmix
```

This will create a file named `mdmix-output-YYYY-MM-DD_HH-MM-SS.md` in the current directory.

### Recursive Mode

To include Markdown files from all subdirectories:

```bash
mdmix -r
```

## Output Format

The generated file includes:

1. **Table of Contents** - Links to each document
2. **Document Sections** - Each file is wrapped in `<document></document>` tags
3. **Folder Information** - When using recursive mode, folder paths are included in `<folder></folder>` tags

Example output structure:

```markdown
# Table of Contents

1. [First Document Title](#path-to-first-document)
2. [Second Document Title](#path-to-second-document)
...

<document id="path-to-first-document">
## File: path/to/first/document.md

<folder>path/to/first</folder>

Content of the first document...
</document>

<document id="path-to-second-document">
## File: path/to/second/document.md

<folder>path/to/second</folder>

Content of the second document...
</document>
```

## Use Cases

- Combining project documentation
- Creating a single reference document from multiple notes
- Preparing Markdown content for export to other formats
- Archiving related Markdown files

## Requirements

- Python 3.6 or higher
