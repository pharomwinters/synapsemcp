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
# tools/advanced_tools.py
"""
Advanced Tools for Synapse

This module contains advanced analysis and processing tools that are automatically
discovered by the Synapse system using the @mcp_tool decorator.

These tools demonstrate the auto-discovery system and provide additional
functionality beyond the core server capabilities.
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

# Import the mcp_tool decorator for auto-discovery
from synapse.utils.helpers import mcp_tool

@mcp_tool
def analyze_project_structure(directory_path: Union[str, Path] = ".") -> Dict[str, Any]:
    """
    Analyze the structure of a project directory and provide insights.
    
    Args:
        directory_path: Path to the directory to analyze
        
    Returns:
        Dictionary containing project structure analysis
    """
    try:
        directory_path = Path(directory_path).resolve()
        
        if not directory_path.exists() or not directory_path.is_dir():
            return {"error": f"Directory not found: {directory_path}"}
        
        analysis = {
            "directory": str(directory_path),
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "largest_files": [],
            "synapse_files": [],
            "recent_files": [],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Analyze directory contents
        for item in directory_path.rglob("*"):
            if item.is_file():
                analysis["total_files"] += 1
                
                # File type analysis
                suffix = item.suffix.lower() if item.suffix else "no_extension"
                analysis["file_types"][suffix] = analysis["file_types"].get(suffix, 0) + 1
                
                # File size analysis
                try:
                    size = item.stat().st_size
                    analysis["largest_files"].append({
                        "path": str(item.relative_to(directory_path)),
                        "size": size,
                        "size_mb": round(size / (1024 * 1024), 2)
                    })
                except (OSError, PermissionError):
                    pass
                
                # Check for Synapse files
                if item.name.startswith("synapse_") or item.name in [
                    "projectbrief.md", "requirements.md", "architecture.md",
                    "timeline.md", "meeting_notes.md", "research.md",
                    "testing.md", "deployment.md", "notes.md"
                ]:
                    analysis["synapse_files"].append(str(item.relative_to(directory_path)))
                
                # Recent files (modified in last 7 days)
                try:
                    modified_time = datetime.fromtimestamp(item.stat().st_mtime)
                    if modified_time > datetime.now() - timedelta(days=7):
                        analysis["recent_files"].append({
                            "path": str(item.relative_to(directory_path)),
                            "modified": modified_time.isoformat()
                        })
                except (OSError, PermissionError):
                    pass
                    
            elif item.is_dir():
                analysis["total_directories"] += 1
        
        # Sort largest files by size (top 10)
        analysis["largest_files"] = sorted(
            analysis["largest_files"], 
            key=lambda x: x["size"], 
            reverse=True
        )[:10]
        
        # Sort recent files by modification time
        analysis["recent_files"] = sorted(
            analysis["recent_files"],
            key=lambda x: x["modified"],
            reverse=True
        )[:10]
        
        return analysis
        
    except Exception as e:
        return {"error": f"Failed to analyze project structure: {str(e)}"}

@mcp_tool
def generate_file_checksum(file_path: Union[str, Path], algorithm: str = "sha256") -> Dict[str, Any]:
    """
    Generate checksum for a file using specified algorithm.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        Dictionary containing checksum information
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            return {"error": f"File not found: {file_path}"}
        
        # Validate algorithm
        if algorithm not in ["md5", "sha1", "sha256", "sha512"]:
            return {"error": f"Unsupported algorithm: {algorithm}"}
        
        # Generate checksum
        hash_obj = hashlib.new(algorithm)
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        checksum = hash_obj.hexdigest()
        
        # Get file info
        stat = file_path.stat()
        
        return {
            "file_path": str(file_path),
            "algorithm": algorithm,
            "checksum": checksum,
            "file_size": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Failed to generate checksum: {str(e)}"}

@mcp_tool
def search_text_in_files(
    search_term: str, 
    directory_path: Union[str, Path] = ".", 
    file_extensions: Optional[List[str]] = None,
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Search for text across multiple files in a directory.
    
    Args:
        search_term: Text to search for
        directory_path: Directory to search in
        file_extensions: List of file extensions to include (e.g., ['.py', '.md'])
        case_sensitive: Whether search should be case sensitive
        
    Returns:
        Dictionary containing search results
    """
    try:
        directory_path = Path(directory_path).resolve()
        
        if not directory_path.exists() or not directory_path.is_dir():
            return {"error": f"Directory not found: {directory_path}"}
        
        if not search_term:
            return {"error": "Search term cannot be empty"}
        
        # Default to common text file extensions if none specified
        if file_extensions is None:
            file_extensions = ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.ts', '.html', '.css']
        
        search_results = {
            "search_term": search_term,
            "directory": str(directory_path),
            "case_sensitive": case_sensitive,
            "file_extensions": file_extensions,
            "matches": [],
            "files_searched": 0,
            "total_matches": 0,
            "search_timestamp": datetime.now().isoformat()
        }
        
        # Prepare search term
        search_text = search_term if case_sensitive else search_term.lower()
        
        # Search through files
        for file_path in directory_path.rglob("*"):
            if not file_path.is_file():
                continue
                
            # Check file extension
            if file_path.suffix.lower() not in [ext.lower() for ext in file_extensions]:
                continue
            
            try:
                search_results["files_searched"] += 1
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                file_matches = []
                for line_num, line in enumerate(lines, 1):
                    search_line = line if case_sensitive else line.lower()
                    if search_text in search_line:
                        file_matches.append({
                            "line_number": line_num,
                            "line_content": line.strip(),
                            "context": {
                                "before": [l.strip() for l in lines[max(0, line_num-2):line_num-1]] if line_num > 1 else [],
                                "after": [l.strip() for l in lines[line_num:min(len(lines), line_num+2)]] if line_num < len(lines) else []
                            }
                        })
                
                if file_matches:
                    search_results["matches"].append({
                        "file_path": str(file_path.relative_to(directory_path)),
                        "match_count": len(file_matches),
                        "matches": file_matches[:10]  # Limit to first 10 matches per file
                    })
                    search_results["total_matches"] += len(file_matches)
                    
            except (UnicodeDecodeError, PermissionError, OSError):
                # Skip files that can't be read
                continue
        
        return search_results
        
    except Exception as e:
        return {"error": f"Failed to search text in files: {str(e)}"}

@mcp_tool
def compare_synapse_templates(template_name: str) -> Dict[str, Any]:
    """
    Compare a Synapse template with existing project files and suggest improvements.
    
    Args:
        template_name: Name of the template to compare against
        
    Returns:
        Dictionary containing comparison results and suggestions
    """
    try:
        # Define some basic templates for comparison
        BASIC_TEMPLATES = {
            "projectbrief.md": {
                "description": "Project brief template",
                "content": """# Project Brief

## Overview
[Project description]

## Goals
- Goal 1
- Goal 2

## Requirements
- Requirement 1
- Requirement 2

## Timeline
[Project timeline]
"""
            },
            "requirements.md": {
                "description": "Requirements template", 
                "content": """# Requirements

## Functional Requirements
- FR1: [Description]
- FR2: [Description]

## Non-Functional Requirements
- NFR1: [Description]
- NFR2: [Description]

## Technical Requirements
- TR1: [Description]
- TR2: [Description]
"""
            }
        }
        
        if template_name not in BASIC_TEMPLATES:
            return {"error": f"Template '{template_name}' not found. Available templates: {list(BASIC_TEMPLATES.keys())}"}
        
        template = BASIC_TEMPLATES[template_name]
        template_content = template["content"]
        
        # Look for corresponding file in current directory
        current_file = Path(template_name)
        
        comparison = {
            "template_name": template_name,
            "template_description": template.get("description", ""),
            "current_file_exists": current_file.exists(),
            "comparison_timestamp": datetime.now().isoformat(),
            "suggestions": []
        }
        
        if current_file.exists():
            try:
                with open(current_file, 'r', encoding='utf-8') as f:
                    current_content = f.read()
                
                comparison["current_file_size"] = len(current_content)
                comparison["template_size"] = len(template_content)
                
                # Basic comparison metrics
                current_lines = current_content.splitlines()
                template_lines = template_content.splitlines()
                
                comparison["current_line_count"] = len(current_lines)
                comparison["template_line_count"] = len(template_lines)
                
                # Check for common sections
                template_sections = [line for line in template_lines if line.startswith('#')]
                current_sections = [line for line in current_lines if line.startswith('#')]
                
                missing_sections = set(template_sections) - set(current_sections)
                extra_sections = set(current_sections) - set(template_sections)
                
                if missing_sections:
                    comparison["suggestions"].append({
                        "type": "missing_sections",
                        "message": "Consider adding these sections from the template",
                        "sections": list(missing_sections)
                    })
                
                if extra_sections:
                    comparison["suggestions"].append({
                        "type": "extra_sections", 
                        "message": "These sections are not in the template",
                        "sections": list(extra_sections)
                    })
                
                # Content freshness
                try:
                    modified_time = datetime.fromtimestamp(current_file.stat().st_mtime)
                    days_old = (datetime.now() - modified_time).days
                    
                    if days_old > 30:
                        comparison["suggestions"].append({
                            "type": "freshness",
                            "message": f"File is {days_old} days old - consider updating",
                            "modified_date": modified_time.isoformat()
                        })
                except (OSError, PermissionError):
                    pass
                    
            except (UnicodeDecodeError, PermissionError, OSError) as e:
                comparison["error"] = f"Could not read current file: {str(e)}"
        else:
            comparison["suggestions"].append({
                "type": "missing_file",
                "message": f"Consider creating {template_name} from template",
                "template_available": True
            })
        
        return comparison
        
    except Exception as e:
        return {"error": f"Failed to compare with template: {str(e)}"}

@mcp_tool
def analyze_synapse_health() -> Dict[str, Any]:
    """
    Analyze the health and completeness of the current Synapse setup.
    
    Returns:
        Dictionary containing health analysis and recommendations
    """
    try:
        health_report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "core_files": {},
            "context_files": {},
            "recommendations": [],
            "statistics": {}
        }
        
        # Define expected core files
        core_files = [
            "synapse_instructions.md",
            "projectbrief.md", 
            "requirements.md",
            "architecture.md"
        ]
        
        # Define optional context files
        context_files = [
            "timeline.md",
            "meeting_notes.md",
            "research.md",
            "testing.md",
            "deployment.md",
            "notes.md"
        ]
        
        current_dir = Path(".")
        
        # Check core files
        core_files_present = 0
        for file_name in core_files:
            file_path = current_dir / file_name
            exists = file_path.exists()
            
            file_info = {
                "exists": exists,
                "path": str(file_path)
            }
            
            if exists:
                core_files_present += 1
                try:
                    stat = file_path.stat()
                    file_info.update({
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "is_empty": stat.st_size == 0
                    })
                    
                    if stat.st_size == 0:
                        health_report["recommendations"].append({
                            "type": "empty_core_file",
                            "message": f"Core file {file_name} is empty",
                            "priority": "high"
                        })
                except (OSError, PermissionError):
                    pass
            else:
                health_report["recommendations"].append({
                    "type": "missing_core_file",
                    "message": f"Core file {file_name} is missing",
                    "priority": "high"
                })
            
            health_report["core_files"][file_name] = file_info
        
        # Check context files
        context_files_present = 0
        for file_name in context_files:
            file_path = current_dir / file_name
            exists = file_path.exists()
            
            file_info = {
                "exists": exists,
                "path": str(file_path)
            }
            
            if exists:
                context_files_present += 1
                try:
                    stat = file_path.stat()
                    file_info.update({
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except (OSError, PermissionError):
                    pass
            
            health_report["context_files"][file_name] = file_info
        
        # Calculate statistics
        health_report["statistics"] = {
            "core_files_present": core_files_present,
            "core_files_total": len(core_files),
            "core_completion_percentage": (core_files_present / len(core_files)) * 100,
            "context_files_present": context_files_present,
            "context_files_total": len(context_files),
            "context_completion_percentage": (context_files_present / len(context_files)) * 100
        }
        
        # Determine overall health
        core_percentage = health_report["statistics"]["core_completion_percentage"]
        if core_percentage == 100:
            health_report["overall_health"] = "excellent"
        elif core_percentage >= 75:
            health_report["overall_health"] = "good"
        elif core_percentage >= 50:
            health_report["overall_health"] = "fair"
        else:
            health_report["overall_health"] = "poor"
        
        # Add general recommendations
        if core_percentage < 100:
            health_report["recommendations"].append({
                "type": "core_completion",
                "message": f"Complete core Synapse files for optimal functionality ({core_percentage:.0f}% complete)",
                "priority": "medium"
            })
        
        if context_files_present == 0:
            health_report["recommendations"].append({
                "type": "context_files",
                "message": "Consider adding context files to enhance project documentation",
                "priority": "low"
            })
        
        return health_report
        
    except Exception as e:
        return {"error": f"Failed to analyze Synapse health: {str(e)}"}

# Note: These tools will be automatically discovered by the Synapse system
# when auto-discovery is enabled. They demonstrate advanced functionality
# that extends beyond the core server capabilities. 