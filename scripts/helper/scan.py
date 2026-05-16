from pathlib import Path

from .tools import PLACEHOLDERS, normalize

def is_empty(text: str) -> tuple[bool, dict]:
    stripped = text.strip()
    frontmatter = []

    if not stripped:
        return True, {"empty": True}

    lines = [
        line.strip()
        for line in stripped.splitlines()
        if line.strip()
    ]
    
    # strip frontmatter
    if len(lines) > 1 and lines[0] == "---":
        end = lines.index("---", 1)
        frontmatter = lines[:end+1]
        lines = lines[end + 1:]

    # title only
    if len(lines) == 1 and lines[0].startswith("#"):
        return True, {"empty": True, "frontmatter": frontmatter}

    # placeholder only
    joined = normalize(" ".join(lines))
    if joined in PLACEHOLDERS:
        return True, {"empty": True, "frontmatter": frontmatter}

    if any("FILL-INFO" in line for line in lines):
        sections = []
        current_section = "Unknown"
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#"):
                current_section = line.lstrip("#").strip()
            if "FILL-INFO" in line:
                para = [line.replace("FILL-INFO:", "").replace("FILL-INFO", "").strip()]
                i+=1
                while i < len(lines) and not lines[i].startswith("#"):
                    para.append(lines[i])
                    i += 1
                sections.append({
                    "section": current_section,
                    "hints": " ".join(para) if para else "",
                })
                i -= 1 # skipped one too far
            i += 1
        return True, {"empty": False, "section-changes": sections, "frontmatter": frontmatter}

    return False, {}

def vault(path: Path, index: list[Path] = []):
    if len(index)==0: index = sorted(path.rglob("*.md"))
    else: index = [p for p in index if p.suffix == ".md"]
    for p in index:
        try:
            content = p.read_text(encoding="utf-8")
        except Exception as e:
            print( f"error at {str(path)}: {str(e)}")
            continue
        fillable, x = is_empty(p.read_text(encoding="utf-8"))
        if fillable:
            result = {"path": str(p)}
            result.update(x) # This way to have the path first
            yield result
