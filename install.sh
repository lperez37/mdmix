#!/usr/bin/env bash

# MDMix Installation Script
# This script installs mdmix as a command-line tool

set -e

echo "🚀 Installing MDMix..."

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MDMIX_SCRIPT="$SCRIPT_DIR/mdmix.py"

# Check if mdmix.py exists
if [ ! -f "$MDMIX_SCRIPT" ]; then
    echo "❌ Error: mdmix.py not found in $SCRIPT_DIR"
    exit 1
fi

# Make the Python script executable
echo "📝 Making mdmix.py executable..."
chmod +x "$MDMIX_SCRIPT"

# Create ~/.local/bin if it doesn't exist
LOCAL_BIN="$HOME/.local/bin"
if [ ! -d "$LOCAL_BIN" ]; then
    echo "📁 Creating $LOCAL_BIN directory..."
    mkdir -p "$LOCAL_BIN"
fi

# Create symlink
SYMLINK_PATH="$LOCAL_BIN/mdmix"
echo "🔗 Creating symlink at $SYMLINK_PATH..."

# Remove existing symlink if it exists
if [ -L "$SYMLINK_PATH" ]; then
    rm "$SYMLINK_PATH"
fi

# Create the symlink
ln -sf "$MDMIX_SCRIPT" "$SYMLINK_PATH"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo "⚠️  ~/.local/bin is not in your PATH"
    echo "   Adding it to your shell configuration..."
    
    # Detect shell and add to appropriate config file
    if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
        SHELL_NAME="zsh"
    elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
        SHELL_NAME="bash"
    else
        SHELL_CONFIG="$HOME/.profile"
        SHELL_NAME="shell"
    fi
    
    # Add PATH export if not already present
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        echo "   Added PATH export to $SHELL_CONFIG"
    fi
    
    echo "   Please run: source $SHELL_CONFIG"
    echo "   Or restart your terminal to use the 'mdmix' command"
else
    echo "✅ ~/.local/bin is already in your PATH"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  mdmix           # Combine markdown files in current directory"
echo "  mdmix -r        # Combine markdown files recursively"
echo ""
echo "Test the installation:"
echo "  mdmix --help"