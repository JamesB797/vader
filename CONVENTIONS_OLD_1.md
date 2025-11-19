- Use :param :return syntax for docstrings
- Do not add redundant "developer commentary" comments, that describe the action
  you are taking, such as `import os  # Add os import`. These clutter the source
  code. Comments are for people who come later to understand why things were
  done a certain way, when important.
- Prefer simpler and shorter code where possible.
- Avoid premature abstraction
- Always batch DB and network calls where possible
- Avoid excessive logging and exception handling unless it is explicitly requested
- End of line comments should be avoided unless they're extremely short. Prefer
  placing comments above the line they refer to, or using docstrings, including
  for variables.