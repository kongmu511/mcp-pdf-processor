# Installation & Setup Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/kongmu511/mcp-pdf-processor.git
cd mcp-pdf-processor
```

### 2. Install Dependencies

**Install PDF utilities:**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Fedora/RHEL
sudo dnf install poppler-utils

# Windows
choco install poppler
```

**Install Python package:**
```bash
pip install -e .
```

### 3. Configure Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json` (macOS/Linux):
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/mcp-pdf-processor/pdf_processor_server.py"]
    }
  }
}
```

Or on Windows (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp-pdf-processor\\pdf_processor_server.py"]
    }
  }
}
```

### 4. Restart Claude Desktop

Close and reopen Claude Desktop. The PDF processing tools should now be available.

## Testing

Ask Claude:
> Extract the text from `/path/to/your/document.pdf`

The agent should now have access to the PDF processing tools.
