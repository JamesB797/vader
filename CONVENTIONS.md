- Use :param :return syntax for docstrings
- DO NOT add comments, print statements, or exception handling unless
  explicitly requested.
- Prefer simpler and shorter code where possible, and avoid premature abstraction
- Always batch DB and network calls where possible
- Using os.environ[] means I want it to crash on missing, otherwise I'd use
  os.getenv(). Don't change it.
- For firestore, don't use snapshot's .get() method, use the .to_dict() method instead.
- Flet ft.colors and ft.icons have been renamed to ft.Colors and ft.Icons