#
# This file is part of Synapse.
#
# Synapse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Synapse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Synapse.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Template Server - Template generation and project analysis for Synapse.

This server handles template generation, project analysis, and provides
structured approaches to common tasks in the Synapse system.
"""

from fastmcp import FastMCP
from pathlib import Path
from typing import Dict, List, Optional
import os

# Local imports
from utils import get_db_instance, MemoryFileSystem

# Import templates
from synapse_instructions import TEMPLATE as SYNAPSE_INSTRUCTIONS_TEMPLATE

# Create Template Server instance
template_server = FastMCP("Template Synapse")

# Template definitions - these could be loaded from files or database
TEMPLATES = {
    "synapse_instructions.md": SYNAPSE_INSTRUCTIONS_TEMPLATE,
    "projectbrief.md": """# Project Brief: {project_name}

## Overview
Brief description of the project and its purpose.

## Objectives
- Primary objective 1
- Primary objective 2
- Primary objective 3

## Scope
What is included and excluded in this project.

## Key Requirements
- Requirement 1
- Requirement 2
- Requirement 3

## Timeline
- Phase 1: [Description]
- Phase 2: [Description]
- Phase 3: [Description]

## Resources
- Resource 1
- Resource 2
- Resource 3

## Success Criteria
How will success be measured?

## Risks and Mitigation
- Risk 1: Mitigation strategy
- Risk 2: Mitigation strategy
""",
}

@template_server.tool()
def generate_synapse_template(file_name: str) -> str:
    """Generate a template for a specific Synapse file.
    
    Args:
        file_name: Name of the file to generate template for (e.g., 'projectbrief.md')
        
    Returns:
        Generated template content
    """
    if file_name in TEMPLATES:
        return TEMPLATES[file_name]
    else:
        return f"No template available for '{file_name}'. Available templates: {', '.join(TEMPLATES.keys())}"

@template_server.tool()
def list_available_templates() -> Dict[str, str]:
    """List all available Synapse templates with their descriptions."""
    return {
        "synapse_instructions.md": "Core instructions for using the Synapse system",
        "projectbrief.md": "Template for project brief documentation",
        "analysis.md": "Template for analysis and research documentation",
        "meeting_notes.md": "Template for meeting notes and action items",
        "requirements.md": "Template for requirements specification",
        "architecture.md": "Template for architecture documentation",
        "testing.md": "Template for testing plans and results",
        "deployment.md": "Template for deployment guides and procedures"
    }

@template_server.tool()
def analyze_project_summary(project_summary: str) -> str:
    """Analyze a project summary and provide suggestions for Synapse content.
    
    Args:
        project_summary: Summary of the project to analyze
        
    Returns:
        Suggestions for Synapse structure and content
    """
    return f"""Based on your project summary, here are suggestions for your Synapse:

**Recommended Files:**
1. `synapse_instructions.md`
2. `projectbrief.md` 
3. `requirements.md`
4. `architecture.md`

**Key Points to Include:**
- Project objectives and scope
- Technical requirements and constraints  
- Architecture decisions and rationale
- Timeline and milestones
- Success criteria and metrics

**Next Steps:**
1. Start with the project brief template
2. Define your requirements clearly
3. Document your architecture decisions
4. Create a timeline with key milestones

**Project Summary Analysis:**
{project_summary}

**Suggestions:**
- Consider breaking down complex requirements into smaller, manageable components
- Document any assumptions and dependencies early
- Plan for regular review and updates of your Synapse content
- Include risk assessment and mitigation strategies

Would you like me to generate any of these templates for you?"""

@template_server.tool()
def create_project_structure(project_name: str) -> List[str]:
    """Create a complete project structure with templates.
    
    Args:
        project_name: Name of the project
        
    Returns:
        List of created files and their status
    """
    results = []
    
    # Define the basic project structure
    basic_files = [
        "synapse_instructions.md",
        "projectbrief.md",
        "requirements.md", 
        "architecture.md",
        "timeline.md",
        "notes.md"
    ]
    
    try:
        db = get_db_instance()
        
        for file_name in basic_files:
            if file_name in TEMPLATES:
                content = TEMPLATES[file_name]
                if "{project_name}" in content:
                    content = content.replace("{project_name}", project_name)
                    
                success = db.save_memory(file_name, content)
                if success:
                    results.append(f"✅ Created {file_name}")
                else:
                    results.append(f"❌ Failed to create {file_name}")
            else:
                # Create a basic template for files without predefined templates
                content = f"# {file_name.replace('.md', '').replace('_', ' ').title()}\n\n## {project_name}\n\n<!-- Add your content here -->\n"
                success = db.save_memory(file_name, content)
                if success:
                    results.append(f"✅ Created {file_name} (basic template)")
                else:
                    results.append(f"❌ Failed to create {file_name}")
                    
    except Exception as e:
        results.append(f"❌ Error creating project structure: {str(e)}")
        
    return results

# Export the server
__all__ = ["template_server"] 