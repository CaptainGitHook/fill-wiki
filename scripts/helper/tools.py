PLACEHOLDERS = {
        "",
        "todo",
        "tbd",
        "stub",
        "wip",
}

LINKABLE_EXTENSIONS = {
    '.md', '.pdf',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
    '.mp3', '.wav', '.ogg', '.mp4', '.mov', '.avi',
    '.csv',
}

def normalize(text: str) -> str:
    return text.strip().lower()
