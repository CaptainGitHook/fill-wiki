from pathlib import Path

from .tools import LINKABLE_EXTENSIONS

def build(root_dir: Path = Path(".")) -> list[Path]:
    files = []
    for entry in root_dir.rglob("*"):
        if entry.is_file() and entry.suffix.lower() in LINKABLE_EXTENSIONS:
            files.append(entry.resolve())
    return files
