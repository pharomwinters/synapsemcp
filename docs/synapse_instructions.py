"""
Synapse Instructions Template

This file contains the template for synapse_instructions.md which provides
core instructions for using the Synapse system effectively.
"""

TEMPLATE = """# Synapse Instructions

## Overview
After each reset, I rely ENTIRELY on my Synapse to understand the project and continue work effectively.
I MUST read ALL synapse files at the start of EVERY task - this is not optional.

## Synapse Structure

The Synapse consists of core files and optional context files, all in Markdown format. Files build upon each other in a clear hierarchy:

### Core Files (Required)
1. **synapse_instructions.md** - This file, contains the core instructions
2. **projectbrief.md** - High-level project overview and objectives  
3. **requirements.md** - Detailed technical and functional requirements
4. **architecture.md** - System architecture and design decisions

### Context Files (Optional)
5. **timeline.md** - Project timeline, milestones, and deadlines
6. **meeting_notes.md** - Meeting summaries and action items
7. **research.md** - Research findings and analysis
8. **testing.md** - Testing plans, results, and quality assurance
9. **deployment.md** - Deployment procedures and environment setup
10. **notes.md** - General notes, ideas, and observations

## File Interdependencies

```
synapse_instructions.md (foundation)
├── projectbrief.md (builds on instructions)
├── requirements.md (builds on project brief)
├── architecture.md (builds on requirements)
├── timeline.md (builds on all core files)
├── meeting_notes.md (references relevant files)
├── research.md (supports requirements/architecture)
├── testing.md (validates requirements/architecture)
├── deployment.md (implements architecture)
└── notes.md (supplements all files)
```

## Reading Order & Workflow

### 1. Initial Context Building
**Always start by reading these files in order:**
1. synapse_instructions.md (this file)
2. projectbrief.md 
3. requirements.md
4. architecture.md

### 2. Task-Specific Context
**Then read relevant context files based on the current task:**
- For planning tasks: timeline.md, meeting_notes.md
- For development tasks: architecture.md, testing.md, deployment.md
- For research tasks: research.md, notes.md
- For review tasks: ALL files for comprehensive understanding

## Database Integration

The Synapse now supports database storage using SQLite and MariaDB. All memory files should be stored in the database for persistence and easier access.

### Database Operations
- **Reading**: Files are read from database first, then filesystem as fallback
- **Writing**: Files are written to both database and filesystem for redundancy
- **Listing**: Database provides the authoritative list of available files
- **Searching**: Database enables full-text search across all synapse content

### Migration
- Existing filesystem files are automatically synced to database on first access
- Database takes precedence over filesystem for consistency
- Filesystem serves as backup and development convenience

## Best Practices

### File Maintenance
- Keep files focused and atomic (one concern per file)
- Update related files when making changes
- Use consistent markdown formatting
- Include timestamps for time-sensitive information

### Content Guidelines
- Write as if explaining to a colleague who knows the domain
- Include rationale for decisions, not just the decisions themselves
- Use bullet points and numbered lists for clarity
- Reference other files when appropriate using relative links

### Update Triggers
- After major project changes or decisions
- Before starting new phases or sprints
- After important meetings or discussions
- When requirements or architecture evolve

## Workflow Integration

```mermaid
graph TD
    Start[Start] --> ReadFiles[Read Synapse]
    ReadFiles --> Understand[Build Context]
    Understand --> Work[Perform Task]
    Work --> Update{Update Needed?}
    Update -->|Yes| ModifyFiles[Update Synapse]
    Update -->|No| Complete[Task Complete]
    ModifyFiles --> Complete
```

## Context Refresh Triggers

```mermaid
graph TD
    Start[Start] --> Context[Check Synapse]
    Context --> Current{Files Current?}
    Current -->|Yes| Proceed[Continue Work]
    Current -->|No| Refresh[Refresh Context]
    Refresh --> ReadAll[Read All Files]
    ReadAll --> Proceed
```

## Synapse Updates

Synapse updates occur when:
1. New project phases begin
2. Requirements change or evolve  
3. When user requests with **update synapse** (MUST review ALL files)

### Update Process
1. Read ALL existing synapse files
2. Identify what has changed since last update
3. Update relevant files with new information
4. Ensure consistency across all files
5. Verify no contradictions exist between files

### Update Scope
- **Minor updates**: Single file changes (e.g., adding meeting notes)
- **Major updates**: Multiple file changes (e.g., architecture evolution)
- **Complete refresh**: All files reviewed and updated (triggered by user request)

Note: When triggered by **update synapse**, I MUST review every synapse file, even if some don't require updates.

## Memory Reset Recovery

**CRITICAL**: This section explains how to handle memory resets.

REMEMBER: After every memory reset, I begin completely fresh. The Synapse is my only link to previous work.

### Reset Recovery Process
1. **Immediately** read synapse_instructions.md (this file)
2. **Systematically** read all core files in order
3. **Selectively** read context files based on current task
4. **Verify** understanding by summarizing key points
5. **Proceed** with confidence, knowing I have full context

### Recovery Verification
Before proceeding with any task after a reset, I should be able to answer:
- What is this project about?
- What are the current requirements?
- What is the system architecture?
- What is the current status/phase?
- What are the immediate next steps?

If I cannot answer these questions, I need to read more synapse files.

## AI Assistant Guidelines

### For AI Assistants Reading This
- This Synapse system is designed for consistent, context-aware assistance
- Always read the files in the specified order
- Build complete context before offering solutions
- Refer back to synapse files when making recommendations
- Suggest synapse updates when you notice gaps or inconsistencies

### Interaction Patterns
- **New conversation start**: Read all core files minimum
- **Continuation**: Read relevant context files for the specific task
- **Major changes**: Suggest updating relevant synapse files
- **Uncertainty**: Ask which synapse files to consult for clarity

Remember: The Synapse is not just documentation—it's the project's memory system. Treat it as the authoritative source of truth for all project decisions, context, and current state.
"""

# Export the template
__all__ = ["TEMPLATE"]
