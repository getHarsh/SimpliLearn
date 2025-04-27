#!/usr/bin/env python3
"""
Project Management MCP Server
--------------------------
An MCP server implementation that provides project management templates to Claude Desktop.
This server follows the Model Context Protocol (MCP) and provides tools for Claude to access
and use project management templates.

Author: Harsh
Website: https://www.getharsh.in
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Configure logging to stderr only to avoid polluting stdout with non-JSON
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("mcp_project_manager")

# Import MCP SDK
from mcp.server.fastmcp import FastMCP

# Define the template directory - using the existing path (DRY principle)
CURRENT_DIR = Path(__file__).parent
PROMPT_TEMPLATE_DIR = CURRENT_DIR.parent / "source_code" / "prompt_templates"

# Ensure the template directory exists
if not PROMPT_TEMPLATE_DIR.exists():
    logger.warning(f"Template directory not found at {PROMPT_TEMPLATE_DIR}")
    # Fallback to a templates directory in the current folder
    PROMPT_TEMPLATE_DIR = CURRENT_DIR / "templates"
    os.makedirs(PROMPT_TEMPLATE_DIR, exist_ok=True)
    logger.info(f"Created fallback template directory at {PROMPT_TEMPLATE_DIR}")

# Template categories with descriptions
TEMPLATE_CATEGORIES = {
    "system": "Base templates establishing Claude's role as a PM consultant",
    "planning": "Templates for project planning, scope definition, and scheduling",
    "tracking": "Templates for progress tracking and status reporting",
    "risk": "Templates for risk identification and mitigation strategies",
    "collaboration": "Templates for team collaboration and stakeholder management",
    "general": "Templates for general project management queries"
}

# Create MCP server with protocol version
mcp = FastMCP(
    "Project Management Assistant", 
    protocol_version="2024-11-05",
    # Add initialize response directly in the constructor
    initialize_response={
        "capabilities": {
            "textDocumentSync": 2,
            "experimental": {
                "sessionManager": True,
                "keepAlive": True
            }
        },
        "serverInfo": {
            "name": "Project Management Assistant",
            "version": "1.0.0",
            "protocolVersion": "2024-11-05"
        }
    }
)

# Utility Functions
async def list_prompt_templates() -> List[str]:
    """List all available prompt templates in the template directory."""
    templates = []
    try:
        for file in PROMPT_TEMPLATE_DIR.glob("*.md"):
            templates.append(file.stem)
        return templates
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        return []

async def load_prompt_template(template_name: str) -> Optional[str]:
    """Load a specific prompt template by name."""
    try:
        template_path = PROMPT_TEMPLATE_DIR / f"{template_name}.md"
        if template_path.exists():
            return template_path.read_text()
        else:
            logger.warning(f"Template not found: {template_name}")
            return None
    except Exception as e:
        logger.error(f"Error loading template {template_name}: {e}")
        return None

async def generate_prompt(template_name: str, variables: Dict[str, str] = None) -> Optional[str]:
    """Generate a prompt by replacing variables in a template."""
    template_content = await load_prompt_template(template_name)
    if not template_content:
        return None
        
    if variables:
        for key, value in variables.items():
            template_content = template_content.replace(f"[{key}]", value)
    
    return template_content

# MCP Tool: List Templates
@mcp.tool()
async def list_templates() -> List[str]:
    """List all available project management templates."""
    try:
        templates = await list_prompt_templates()
        return templates
    except Exception as e:
        logger.error(f"Error in list_templates: {e}")
        return []

# MCP Tool: Get Template
@mcp.tool()
async def get_template(name: str) -> Dict[str, Any]:
    """Get a specific project management template by name."""
    try:
        template_content = await load_prompt_template(name)
        if template_content:
            # Extract category from template name if possible
            category = "general"
            for cat in TEMPLATE_CATEGORIES.keys():
                if cat in name.lower():
                    category = cat
                    break
                    
            return {
                "name": name,
                "template": template_content,
                "category": category,
                "variables": [var[1:-1] for var in template_content.split() if var.startswith("[") and var.endswith("]")]
            }
        else:
            return {"error": f"Template '{name}' not found"}
    except Exception as e:
        logger.error(f"Error in get_template: {e}")
        return {"error": f"Failed to get template: {str(e)}"}

# MCP Tool: Generate Prompt from Template
@mcp.tool()
async def generate_prompt_from_template(template_name: str, variables: Dict[str, str] = None) -> Dict[str, Any]:
    """Generate a customized prompt by inserting variables into a template."""
    try:
        prompt = await generate_prompt(template_name, variables)
        if prompt:
            return {
                "template": template_name,
                "prompt": prompt,
                "variables_used": variables or {}
            }
        else:
            return {"error": f"Failed to generate prompt: template '{template_name}' not found"}
    except Exception as e:
        logger.error(f"Error in generate_prompt_from_template: {e}")
        return {"error": f"Failed to generate prompt: {str(e)}"}

# MCP Tool: Get Template Categories
@mcp.tool()
async def get_template_categories() -> Dict[str, str]:
    """Get all available template categories with descriptions."""
    return TEMPLATE_CATEGORIES

# MCP Tool: Get Usage Guide
@mcp.tool()
async def get_usage_guide() -> Dict[str, Any]:
    """Get a complete guide on using the project management templates with Claude."""
    return {
        "title": "Project Management Templates Usage Guide",
        "description": "How to use project management templates with Claude",
        "steps": [
            "1. List available templates using the list_templates tool",
            "2. Get details about a specific template using the get_template tool",
            "3. Generate a customized prompt by providing variables to the generate_prompt_from_template tool",
            "4. Browse templates by category using the get_template_categories tool"
        ],
        "example": {
            "template": "planning_template",
            "variables": {
                "PROJECT_NAME": "Website Redesign",
                "INDUSTRY": "E-commerce",
                "METHODOLOGY": "Agile"
            }
        },
        "tips": [
            "Templates use placeholders (e.g., [PROJECT_NAME], [INDUSTRY]) that get replaced with your project specifics",
            "You can mix and match templates for different aspects of project management",
            "For general queries, use the general_query_template"
        ]
    }

# Main entry point
if __name__ == "__main__":
    try:
        # Ensure stdout is only used for MCP protocol messages
        sys.stdout.reconfigure(errors='strict')  
        
        # Log startup information to stderr only
        logger.info(f"Starting Project Management MCP Server")
        logger.info(f"Template directory: {PROMPT_TEMPLATE_DIR}")
        
        # Run the MCP server
        mcp.run()
    except Exception as e:
        # Log any errors to stderr, not stdout
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
