#!/usr/bin/env python3
"""MCP server for PDF content extraction and processing."""

import subprocess
import json
import os
from pathlib import Path
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server, RequestContext

# Create server instance
server = Server("pdf-processor")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available PDF processing tools."""
    return [
        types.Tool(
            name="extract_pdf_text",
            description="Extract all text content from a PDF file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the PDF file",
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Maximum lines to extract (optional, default: all)",
                    },
                },
                "required": ["file_path"],
            },
        ),
        types.Tool(
            name="extract_pdf_metadata",
            description="Extract metadata from a PDF file (title, author, pages, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the PDF file",
                    },
                },
                "required": ["file_path"],
            },
        ),
        types.Tool(
            name="extract_pdf_section",
            description="Extract text from a specific page range in a PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the PDF file",
                    },
                    "start_page": {
                        "type": "integer",
                        "description": "Starting page number (1-indexed)",
                    },
                    "end_page": {
                        "type": "integer",
                        "description": "Ending page number (1-indexed, inclusive)",
                    },
                },
                "required": ["file_path", "start_page", "end_page"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    """Handle tool calls."""
    if name == "extract_pdf_text":
        return await extract_pdf_text(
            arguments["file_path"], arguments.get("max_lines")
        )
    elif name == "extract_pdf_metadata":
        return await extract_pdf_metadata(arguments["file_path"])
    elif name == "extract_pdf_section":
        return await extract_pdf_section(
            arguments["file_path"], arguments["start_page"], arguments["end_page"]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")


async def extract_pdf_text(file_path: str, max_lines: int = None) -> dict:
    """Extract text from PDF using pdftotext."""
    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    if not file_path.suffix.lower() == ".pdf":
        return {"error": "File must be a PDF"}

    try:
        result = subprocess.run(
            ["pdftotext", str(file_path), "-"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return {"error": f"PDF extraction failed: {result.stderr}"}

        text = result.stdout

        if max_lines:
            lines = text.split("\n")
            text = "\n".join(lines[:max_lines])

        return {
            "success": True,
            "file_path": str(file_path),
            "text": text,
            "lines": len(text.split("\n")),
        }
    except subprocess.TimeoutExpired:
        return {"error": "PDF extraction timed out"}
    except FileNotFoundError:
        return {
            "error": "pdftotext not found. Install with: brew install poppler (macOS) or apt-get install poppler-utils (Linux)"
        }
    except Exception as e:
        return {"error": f"Error extracting PDF: {str(e)}"}


async def extract_pdf_metadata(file_path: str) -> dict:
    """Extract metadata from PDF using pdfinfo."""
    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    if not file_path.suffix.lower() == ".pdf":
        return {"error": "File must be a PDF"}

    try:
        result = subprocess.run(
            ["pdfinfo", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return {"error": f"Failed to extract metadata: {result.stderr}"}

        # Parse pdfinfo output
        metadata = {}
        for line in result.stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        return {"success": True, "file_path": str(file_path), "metadata": metadata}
    except FileNotFoundError:
        return {
            "error": "pdfinfo not found. Install with: brew install poppler (macOS) or apt-get install poppler-utils (Linux)"
        }
    except Exception as e:
        return {"error": f"Error extracting metadata: {str(e)}"}


async def extract_pdf_section(
    file_path: str, start_page: int, end_page: int
) -> dict:
    """Extract text from specific pages in PDF."""
    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    if not file_path.suffix.lower() == ".pdf":
        return {"error": "File must be a PDF"}

    if start_page < 1 or end_page < start_page:
        return {"error": "Invalid page range"}

    try:
        result = subprocess.run(
            [
                "pdftotext",
                "-f",
                str(start_page),
                "-l",
                str(end_page),
                str(file_path),
                "-",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return {"error": f"PDF extraction failed: {result.stderr}"}

        return {
            "success": True,
            "file_path": str(file_path),
            "pages": f"{start_page}-{end_page}",
            "text": result.stdout,
        }
    except FileNotFoundError:
        return {
            "error": "pdftotext not found. Install with: brew install poppler (macOS) or apt-get install poppler-utils (Linux)"
        }
    except Exception as e:
        return {"error": f"Error extracting PDF: {str(e)}"}


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, mcp.server.stdio.stdio_server.InitializationOptions()
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
