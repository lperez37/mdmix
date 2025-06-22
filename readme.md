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

### Option 1: Quick Install (Recommended)

1. Clone this repository:
   ```bash
   git clone https://github.com/lperez37/mdmix.git
   cd mdmix
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

   If you encounter shell interpreter issues, try:
   ```bash
   bash install.sh
   ```

This will make `mdmix` available as a command from anywhere in your terminal.

### Option 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lperez37/mdmix.git
   cd mdmix
   ```

2. Make the script executable:
   ```bash
   chmod +x mdmix.py
   ```

3. Create a symlink in your local bin directory:
   ```bash
   mkdir -p ~/.local/bin
   ln -sf "$(pwd)/mdmix.py" ~/.local/bin/mdmix
   ```

4. Add ~/.local/bin to your PATH (if not already added):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

   For zsh users:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

### Basic Usage

After installation, run in any directory containing Markdown files:

```bash
mdmix
```

This will create a file named `mdmix-output-YYYY-MM-DD_HH-MM-SS.md` in the current directory.

### Recursive Mode

To include Markdown files from all subdirectories:

```bash
mdmix -r
```

### Help

To see all available options:

```bash
mdmix --help
```

## Output Format

The generated file includes:

1. **Table of Contents** - Links to each document
2. **Document Sections** - Each file is wrapped in `<document></document>` tags
3. **Folder Information** - When using recursive mode, folder paths are included in `<folder></folder>` tags

Example output structure:

```markdown
# Table of Contents

1. [First Document Title](#path-to-first-document) - `path/to/first/document.md`
2. [Second Document Title](#path-to-second-document) - `path/to/second/document.md`
...

<document id="path-to-first-document" source="path/to/first/document.md">
## File: path/to/first/document.md

<folder>path/to/first</folder>
**Directory:** `path/to/first`
**Full Path:** `path/to/first/document.md`

Content of the first document...
</document>

<document id="path-to-second-document" source="path/to/second/document.md">
## File: path/to/second/document.md

<folder>path/to/second</folder>
**Directory:** `path/to/second`
**Full Path:** `path/to/second/document.md`

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
