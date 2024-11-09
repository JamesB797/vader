#!/usr/bin/env python3
"""
Vader - A wrapper script for running aider with repository-specific presets.
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Preset:
    """Represents a preset configuration for aider."""
    files: Optional[List[str]] = None
    read_only: Optional[List[str]] = None
    options: Optional[List[str]] = None

def get_repo_name() -> str:
    """Get the current git repository name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True
        )
        repo_path = Path(result.stdout.strip()).resolve().parent
        return repo_path.name
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository", file=sys.stderr)
        sys.exit(1)

def load_presets() -> Dict:
    """Load presets from the presets.yaml file."""
    vader_dir = Path(__file__).resolve().parent
    presets_file = vader_dir / "presets.yaml"
    
    try:
        with open(presets_file) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Error: Presets file not found at {presets_file}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing presets.yaml: {e}", file=sys.stderr)
        sys.exit(1)

def get_preset(repo_name: str, preset_name: str) -> Preset:
    """Get the specified preset for the repository."""
    presets = load_presets()
    
    if 'projects' not in presets or repo_name not in presets['projects']:
        print(f"Error: No presets found for repository '{repo_name}'", file=sys.stderr)
        sys.exit(1)
    
    if preset_name not in presets['projects'][repo_name]:
        print(f"Error: Preset '{preset_name}' not found for repository '{repo_name}'", file=sys.stderr)
        sys.exit(1)
    
    preset_data = presets['projects'][repo_name][preset_name]
    return Preset(**preset_data)

def build_command(preset: Preset) -> List[str]:
    """Build the aider command with all arguments."""
    cmd = ["aider"]
    
    # Load presets to get defaults
    presets = load_presets()
    
    # Add global defaults
    if 'defaults' in presets and 'options' in presets['defaults']:
        cmd.extend(presets['defaults']['options'])
    
    # Add project-specific defaults
    repo_name = get_repo_name()
    if ('projects' in presets and repo_name in presets['projects'] and 
        'defaults' in presets['projects'][repo_name] and 
        'options' in presets['projects'][repo_name]['defaults']):
        cmd.extend(presets['projects'][repo_name]['defaults']['options'])
    
    # Add preset-specific optional arguments
    if preset.options:
        cmd.extend(preset.options)
    
    # Add read-only files
    if preset.read_only:
        for file in preset.read_only:
            cmd.extend(["--read", file])
    
    # Add files to edit
    cmd.extend(preset.files)
    
    return cmd

def main():
    """Main entry point."""
    # Load environment variables from .env
    vader_dir = Path(__file__).resolve().parent
    load_dotenv(vader_dir / ".env")
    
    repo_name = get_repo_name()
    presets_data = load_presets()
    
    # Start with base command
    cmd = ["aider"]
    
    # Add global defaults
    if 'defaults' in presets_data and 'options' in presets_data['defaults']:
        cmd.extend(presets_data['defaults']['options'])
    
    # Add project defaults
    if ('projects' in presets_data and repo_name in presets_data['projects'] and 
        'defaults' in presets_data['projects'][repo_name]):
        project_defaults = presets_data['projects'][repo_name]['defaults']
        if 'options' in project_defaults:
            cmd.extend(project_defaults['options'])
        if 'files' in project_defaults:
            cmd.extend(project_defaults['files'])
    
    # Process any preset arguments
    preset_names = sys.argv[1:] if len(sys.argv) > 1 else []
    
    for preset_name in preset_names:
        preset = get_preset(repo_name, preset_name)
        if preset.options:
            cmd.extend(preset.options)
        if preset.read_only:
            for file in preset.read_only:
                cmd.extend(["--read", file])
        if preset.files:
            cmd.extend(preset.files)
    
    try:
        os.execvp("aider", cmd)
    except FileNotFoundError:
        print("Error: aider command not found. Is it installed?", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
