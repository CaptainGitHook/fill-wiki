---
name: fill-wiki
description: Fill empty markdown notes in an Obsidian vault with the smallest useful wiki-style explanation, including relevant internal links when appropriate. Only run when the user explicitly asks for it.
compatibility: opencode, pi
---

# /fill-wiki

Scan an Obsidian vault or folder for empty or effectively empty markdown notes, infer the topic from the filename and nearby context, and write a compact wiki-style explanation.

# Usage

```
/fill-wiki                                          # full pipeline on current directory → Obsidian vault
/fill-wiki <path>                                   # full pipeline on specific path
/fill-wiki index <path>                             # scan the vault for any obsidian-linkable files
/fill-wiki scan <path>                              # scan the vault for markdown files
```


# What You Must Do When Invoked

If the user invoked `/fill-wiki --help` or `/fill-wiki -h` (with no other arguments), print the contents of the `# Usage` section above verbatim and stop. Do not run any commands, do not detect files, do not default the path to `.`. Just print the Usage block and return.

If the user invoked `/fill-wiki scan <path>`, `/fill-wiki index <path>`, or `/fill-wiki prepare <path>`, execute one of the following, respectively, and stop:
- `python scripts/fill-wiki.py scan <path>`
- `python scripts/fill-wiki.py index <path>`
- `python scripts/fill-wiki.py prepare <path>`
Do not run or do anything else.

If the user invoked `/fill-wiki <path>`, follow the workflow from `# Workflow` below in order. Do not skip steps.

If no path was given, use `.` (current directory). Do not ask the user for a path.


# Workflow

1. Execute `python scripts/fill-wiki.py prepare <vault_root>` to find all effectively empty and all linkable files in the target vault or folder.
2. For each note or paragraph, infer the topic from:
- titles in the file
- the filename
- parent folder names
- existing internal links in the vault
4. Decide whether the topic is clear enough to fill.
5. Create a minimal wiki-style explanation as explained below, in `## Creating an entry`.
6. Add relevant Obsidian links when useful and unambiguous.
7. Apply the change by executing `python scripts/fill-wiki.py apply <path_to_json>` as explained below, in `## Applying changes to files`.
8. Leave non-empty notes unchanged.
9. Report which files were filled or ambiguous.

## Creating an entry

Executing `python scripts/fill-wiki.py prepare <vault_root>` will produce a JSON-object for all fillable notes and a separate JSON-list for all linkable files in the vault.
If the note is empty:
- Create the entire note for the inferred topic
- Its entry will have this structure:
```
{
    "path": "<path_to_note>",
    "empty": true
    "frontmatter": "<the notes frontmatter>"
},
```

If the note is not empty:
- Create separate sections for each section in `section-changes`
- Use the prompt in the `hints` section if available for recommended section content
- Its entry will have this structure:
```
{
    "path": "<path to note>",
    "empty": false,
    "fill-info": [
        {
            "section": "First Empty Section",
            "hints": "Content hints for the entry."
        },
        {
            "section": "Second Empty Section",
            "hints": ""
        }
    ]
},
```

## Applying changes to files

When ready to apply changes, construct a JSON plan with this schema:
```
{
    "files": [
        {
            "path": "<relative path to note>",
            "changes": [
                {
                    "content": "<full markdown content>"
                }
            ]
        },
        {
            "path": "<relative path to note>",
            "changes": [
                {
                    "section": "<first empty section>",
                    "content": "<section markdown content>"
                },
                {
                    "section": "<second empty section>",
                    "content": "<section markdown content>"
                }
            ]
        }
    ]
}
```
For section-wise changes, the `"section"` entry is required.

When ready confirm with the user. Do not write anything before confirmation.
If confirmed apply the changes by piping this JSON into  `python scripts/fill-wiki.py apply`, via stdin.

Do NOT write to files in any other way.

# Invocation rule

Only use this skill when the user explicitly asks to:
- fill empty notes
- expand stubs
- populate a vault
- write explanations for a set of notes

Do not trigger it automatically from vague file activity or unrelated editing tasks.

# Writing rules

The filled note should be:

- short
- definition-first
- neutral and factual
- self-contained
- written in simple wiki style
- centered on the topic itself
- use LaTex formulas wherever possible

The note should usually contain:
- a one-sentence definition if possible
- 2 to 4 short paragraphs with the main ideas
- key formulas, properties, notation, or examples when useful
- one brief “related concepts” line if helpful

Do not change existing text. Only add to the existing frontmatter, do not remove any of it.

# Naming and frontmatter rules

Names generally follow kebab case.

New note rules:
- Put down a frontmatter with a human-readable id, aliases and tags
- Fill aliases and tags if helpful

Prefer:
- `id: Note Name`

# Linking rules for Obsidian

Use internal links when they are clearly relevant and present in the list of linkable files, or very likely to be produced in the future.

Prefer:
- `[[Related Topic]]`
- `[[Parent Topic]]`
- `[[Common Notation]]`
- `[[Theorem Name]]`
- `[[Algorithm Name]]`

Linking rules:
- Link only when the relation is real and helpful.
- Do not force links into every sentence.
- Prefer existing or obviously intended note titles.
- If a link target is uncertain, leave it unlinked.
- Do not create noisy link chains.

# Style constraints

- Prefer the smallest useful explanations.
- Avoid long introductions.
- Avoid motivational language.
- Avoid speculation.
- Avoid historical digressions.
- Avoid examples unless they clarify the core concept.
- Use standard terminology from mathematics, physics, or computer science.

# Failure handling

If a note cannot be filled safely:
- leave it unchanged
- mark it as ambiguous
- explain the ambiguity briefly
- do not guess
