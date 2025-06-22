#!/usr/bin/env bash

# MDMix Installation Script
# This script installs mdmix as a command-line tool

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    echo "  ███╗   ███╗██████╗ ███╗   ███╗██╗██╗  ██╗"
    echo "  ████╗ ████║██╔══██╗████╗ ████║██║╚██╗██╔╝"
    echo "  ██╔████╔██║██║  ██║██╔████╔██║██║ ╚███╔╝ "
    echo "  ██║╚██╔╝██║██║  ██║██║╚██╔╝██║██║ ██╔██╗ "
    echo "  ██║ ╚═╝ ██║██████╔╝██║ ╚═╝ ██║██║██╔╝ ██╗"
    echo "  ╚═╝     ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝"
    echo -e "${NC}"
    echo -e "${WHITE}${BOLD}    Markdown File Combiner - Installation${NC}"
    echo -e "${PURPLE}    ════════════════════════════════════════${NC}"
    echo ""
}

# Progress animation
show_progress() {
    local message=$1
    echo -ne "${YELLOW}${message}${NC}"
    
    for i in {1..8}; do
        echo -ne "${CYAN}.${NC}"
        sleep 0.1
    done
    echo -e " ${GREEN}✓${NC}"
}

# Success checkmark animation
show_success() {
    local message=$1
    echo -e "${GREEN}✅ ${message}${NC}"
}

# Warning message
show_warning() {
    local message=$1
    echo -e "${YELLOW}⚠️  ${message}${NC}"
}

# Error message
show_error() {
    local message=$1
    echo -e "${RED}❌ ${message}${NC}"
}

print_banner
echo -e "${GREEN}🚀 Starting MDMix installation...${NC}"
echo ""

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MDMIX_SCRIPT="$SCRIPT_DIR/mdmix.py"

# Check if mdmix.py exists
if [ ! -f "$MDMIX_SCRIPT" ]; then
    show_error "mdmix.py not found in $SCRIPT_DIR"
    exit 1
fi

# Make the Python script executable
show_progress "Making mdmix.py executable"
chmod +x "$MDMIX_SCRIPT"

# Create ~/.local/bin if it doesn't exist
LOCAL_BIN="$HOME/.local/bin"
if [ ! -d "$LOCAL_BIN" ]; then
    show_progress "Creating $LOCAL_BIN directory"
    mkdir -p "$LOCAL_BIN"
fi

# Create symlink
SYMLINK_PATH="$LOCAL_BIN/mdmix"
show_progress "Creating symlink at $SYMLINK_PATH"

# Remove existing symlink if it exists
if [ -L "$SYMLINK_PATH" ]; then
    rm "$SYMLINK_PATH"
fi

# Create the symlink
ln -sf "$MDMIX_SCRIPT" "$SYMLINK_PATH"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    show_warning "~/.local/bin is not in your PATH"
    echo -e "   ${BLUE}Adding it to your shell configuration...${NC}"
    
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
        show_success "Added PATH export to $SHELL_CONFIG"
    fi
    
    echo -e "   ${CYAN}Please run: ${WHITE}source $SHELL_CONFIG${NC}"
    echo -e "   ${CYAN}Or restart your terminal to use the 'mdmix' command${NC}"
else
    show_success "~/.local/bin is already in your PATH"
fi

echo ""
echo -e "${GREEN}${BOLD}🎉 Installation complete!${NC}"
echo ""
echo -e "${WHITE}${BOLD}Usage:${NC}"
echo -e "  ${YELLOW}mdmix${NC}           # Combine files in current directory"
echo -e "  ${YELLOW}mdmix -r${NC}        # Combine files recursively"
echo ""
echo -e "${WHITE}${BOLD}Test the installation:${NC}"
echo -e "  ${YELLOW}mdmix --help${NC}"
echo ""