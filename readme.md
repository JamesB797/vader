# Vader

A wrapper script for running [aider](https://github.com/Aider-AI/aider) with
repository-specific presets.

## Installation

1. Clone this repository:
   ```bash
   git clone git@upfeat.dev:james.brown/vader.git
   ```

2. Install required dependencies:
   ```bash
   pip install pyyaml python-dotenv
   ```

3. Add vader's bin directory to your PATH by adding this line to your shell's config file:

   For bash (\~/.bashrc) or zsh (\~/.zshrc):
   ```bash
   export PATH="/path/to/vader/bin:$PATH"
   ```

   For fish (~/.config/fish/config.fish):
   ```fish
   set -x PATH /path/to/vader/bin $PATH
   ```

   Replace `/path/to/vader` with the actual path where you cloned the repository.

4. Reload your shell configuration or restart your terminal.

## Overview

The `vader` command allows you to run aider with predefined sets of options and files
based on the current git repository. It automatically:

1. Determines the current git repository name
2. Loads predefined presets for that repository
3. Sets environment variables from Vader's .env file
4. Launches aider with the specified preset's options and files

## Usage

```bash
vader [preset-name...]
```

The vader command can be run with zero or more preset names:

- `vader` - Uses project defaults only
- `vader es` - Uses project defaults plus the "es" preset
- `vader es docs` - Combines project defaults with both the "es" and "docs" presets

When multiple presets are specified, their options and files are combined in order.

## Configuration

### Presets

Presets are stored in `presets.yaml` in the Vader directory using this structure:

```yaml
defaults:
  options: [ "--vim" ]  # Global default options

projects:
  repository-name:
    defaults:
      options: [ "--language", "python" ]  # Project-specific defaults
    preset-name:
      files: [ "file1.py", "file2.py" ]        # Required: Files to edit
      read_only: [ "config.py", "types.py" ]    # Optional: Files passed with --read
      options: [ "--context-size", "3000" ]     # Optional: Additional aider options
```

Options are applied in this order:

1. Global defaults (from top-level `defaults`)
2. Project defaults (from project's `defaults`)
3. Preset-specific options

### Environment Variables

Environment variables for LLM api keys etc. are loaded from the `.env` file in the Vader
root directory before launching aider.

## Helpful refactoring commands

Without impacting functionality and total information available in the console, reduce the total code and print volume as much as possible. Do not add # comments.
