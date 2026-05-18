
# /fill-wiki

Fill empty markdown notes or sections of notes in an (not necessarily Obsidian) vault with wiki-style explanations.

## Installation

### Prerequisites

- Python 3.10+
- [opencode](https://opencode.ai) or [pi](https://github.com/anomalyco/pi)

### Install the skill

Clone the skill into your opencode skills directory:

```bash
git clone https://github.com/CaptainGitHook/fill-wiki ~/.config/opencode/skills/fill-wiki
```

### Verify

```bash
opencode
# then inside opencode:
#   /fill-wiki --help
```

If you see the usage block, the skill is ready.


## What it does

1. Scans a directory for empty or "effectively" empty `.md` notes or marked subtopics in those notes
2. Infers the topic from filename, frontmatter, folders, and surrounding vault context
3. Writes a minimal, definition-first wiki entry with internal `[[links]]`
4. Applies changes to disk via a structured JSON plan

You can mark empty notes with words like "WIP", "tbd" or "TODO". Notes that have only a title in them count as "effectively empty" as well. Sections to be filled within otherwise populated notes are marked with a `FILL-INFO` (all case insensitive) in the corresponding paragraph.

Hints can be left for the model as well, see `## Usage`.

Notes that are already populated are left untouched. They are searched for and written to deterministically, so no danger of deleting notes due to hallucinations.
Ambiguous or uncertain topics are reported without guessing.

## Usage

| Command | Action |
|---|---|
| `/fill-wiki` | Fill empty notes in current directory (full pipeline) |
| `/fill-wiki <path>` | Fill empty notes in the given vault/directory (full pipeline) |
| |
| Deterministic: |
| `/fill-wiki index <path>` | Scan vault for linkable files (no filling) |
| `/fill-wiki scan <path>` | Scan vault for empty markdown files (no filling) |


If you want to guide the model to fill sensible information, just put down a paragraph into your empty markdown notes like this:
```
FILL-INFO: Here are some hints for the model.
Can be a full paragraph.

Or maybe several, resets at the next headline.
```

The same thing applies to sections of notes. You can leave the hints empty as well
```
# A Paragraph I Have Not Researched Yet

FILL-INFO
```
