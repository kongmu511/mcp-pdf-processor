# MCP PDF Processor

An MCP (Model Context Protocol) server for extracting and processing PDF content. Enables Claude and other AI agents to understand and work with PDF documents directly.

## Features

- **Extract Full PDF Text**: Convert entire PDF documents to plain text
- **Extract PDF Metadata**: Get document properties (title, author, page count, etc.)
- **Extract Specific Pages**: Extract text from a specific page range
- **Timeout Protection**: Prevents hanging on large PDFs
- **Error Handling**: Comprehensive error messages for debugging

## Installation

### Prerequisites

- Python 3.10+
- `pdftotext` and `pdfinfo` utilities

#### Install PDF Tools

**macOS:**
```bash
brew install poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install poppler-utils
```

**Windows:**
```bash
choco install poppler
```

### Setup MCP Server

```bash
git clone https://github.com/yourusername/mcp-pdf-processor.git
cd mcp-pdf-processor
pip install -e .
```

## Usage

### As an MCP Server

Add to your Claude Desktop configuration (`~/.config/Claude/claude_desktop_config.json` on macOS/Linux or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "python",
      "args": ["/path/to/mcp-pdf-processor/pdf_processor_server.py"]
    }
  }
}
```

Then restart Claude Desktop to enable the PDF processing tools.

### Available Tools

#### 1. `extract_pdf_text`
Extract all text content from a PDF file.

**Parameters:**
- `file_path` (string, required): Absolute path to the PDF file
- `max_lines` (integer, optional): Maximum number of lines to extract

**Example:**
```python
{
  "file_path": "/Users/username/documents/sample.pdf",
  "max_lines": 100
}
```

#### 2. `extract_pdf_metadata`
Extract metadata from a PDF file.

**Parameters:**
- `file_path` (string, required): Absolute path to the PDF file

**Example:**
```python
{
  "file_path": "/Users/username/documents/sample.pdf"
}
```

#### 3. `extract_pdf_section`
Extract text from a specific page range.

**Parameters:**
- `file_path` (string, required): Absolute path to the PDF file
- `start_page` (integer, required): Starting page (1-indexed)
- `end_page` (integer, required): Ending page (1-indexed, inclusive)

**Example:**
```python
{
  "file_path": "/Users/username/documents/sample.pdf",
  "start_page": 1,
  "end_page": 10
}
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Format Code

```bash
black pdf_processor_server.py
isort pdf_processor_server.py
```

### Type Check

```bash
mypy pdf_processor_server.py
```

## Architecture

This MCP server implements the Model Context Protocol specification, allowing AI agents to:
1. Discover available PDF processing capabilities via `list_tools()`
2. Extract PDF content using the available tools
3. Process responses in JSON format for further analysis

## Error Handling

The server provides detailed error messages for common issues:
- File not found errors
- Non-PDF file handling
- Missing system utilities (pdftotext/pdfinfo)
- Timeout on large PDFs
- Invalid page ranges

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions, please open a GitHub issue or contact the maintainers.
