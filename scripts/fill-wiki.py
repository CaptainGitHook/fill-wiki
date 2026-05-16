from __future__ import annotations

import sys
import argparse
import json
from pathlib import Path

from helper import scan
from helper import index
from helper import apply


def cmd_scan(args: argparse.Namespace) -> int:
    results = [p for p in scan.vault(Path(args.vault))]
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    idx = [str(p) for p in index.build(Path(args.vault))]
    print(json.dumps(idx, indent=2, ensure_ascii=False))
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    print(f"JSON of all fillable markdown notes:")
    cmd_scan(args)
    print(f"\nJSON of all linkable files in the vault:")
    cmd_index(args)
    return 0

def cmd_apply(args: argparse.Namespace) -> int:
    if args.planfile:
        with open(args.planfile, 'r') as file:
            data = json.load(file)
    else:
        try:
            data = json.load(sys.stdin)
        except Exception as e:
            print(json.dumps({
                "error": f"invalid json: {e}"
            }))
            return 2
    for filechange in data["files"]:
        try:
            print(f"changing {filechange['path']}...")
            apply.changes(filechange)
        except Exception as e:
            print(e)
    return 0

def main() -> int:
    p = argparse.ArgumentParser(prog="fill-empty-notes")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan")
    s.add_argument("vault")
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("index")
    s.add_argument("vault")
    s.set_defaults(func=cmd_index)

    s = sub.add_parser("prepare")
    s.add_argument("vault")
    s.set_defaults(func=cmd_prepare)
    
    s = sub.add_parser("apply")
    s.add_argument('-p', '--planfile', nargs='?', type=argparse.FileType('r'), help='input file, in JSON format')
    s.set_defaults(func=cmd_apply)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
