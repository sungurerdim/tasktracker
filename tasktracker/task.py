from pathlib import Path

class Task:
    def __init__(self, data, name=None, desc=None):
        self.data = data
        path = Path(str(data)) if isinstance(data, (str, Path)) else None
        self.name = name if name else (path.stem if path else str(data)[:16])
        self.desc = desc if desc else (f"Processing '{path.name}'" if path else f"{str(data)[:40]}...")