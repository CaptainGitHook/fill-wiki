from pathlib import Path

from .tools import PLACEHOLDERS, normalize

def changes(c: dict):
    path = Path(c["path"])
    for change in c["changes"]:
        if "section" in change.keys():
            with open(path) as f:
                lines = f.readlines()
            sec = change["section"]
            out = []
            found_sec = False
            for i, l in enumerate(lines):
                stripped = l.lstrip("#").strip()
                if not found_sec and stripped == sec:
                    found_sec = True
                elif found_sec and "fill-info" in normalize(l.strip()):
                    out.append(f"{change['content']}\n\n")
                    out = out + lines[i:]
                    break
                out.append(l)
            if not found_sec:
                print(f"Section {change['section']} not found in {path}!")
                out.append(f"\n\n# {change['section']}\n\n")
                out.append(f"{change['content']}\n\n")
            with open(path, "w") as f:
                f.writelines(out)
        else:
            ## FILE IS EMPTY! Overwrite everything, including frontmatter
            # with open(path) as f:
            #     kept = [l for l in f if l.strip().lower() not in PLACEHOLDERS]
            # kept.append(change["content"])
            with open(path, "w") as f:
                f.write(change["content"])
