"""Regenerate book/ from the author's manuscript repo.

Usage:  python tools/import_from_book.py /path/to/bitcoin-from-scratch

The manuscript repo's notebooks/ already interleave the prose with the code.
This script copies them (and the chapters that have no code) into book/,
with three changes for the web edition:

  1. Outputs are cleared; the site executes every notebook at build time.
  2. A markdown cell that opens with a printed "Output:" block duplicating the
     code cell above it has that block removed (the real output shows instead).
  3. Pages written for the printed book get small web-specific notes.
"""
import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(__file__).resolve().parent.parent / "book"
CODE_REPO = "https://github.com/aaron-recompile/bitcoin-from-scratch-code"

PRINTED_OUTPUT = re.compile(r"^\s*Output:\s*\n+```text\n.*?\n```\s*\n*", re.S)

MD_PAGES = [
    "ch00-prologue.md",
    "ch17-docker-network.md",
    "appendix-a-crypto-map.md",
    "appendix-b-quantum.md",
    "appendix-c-checksig-csfs.md",
]

CH17_NOTE = f"""
:::{{note}} This chapter runs outside the browser
Every other chapter runs right here on the page. This one starts several
processes that talk to each other over HTTP, so it needs a real machine.
The code is in [`toycoin_network/`]({CODE_REPO}/tree/main/toycoin_network).
:::
"""


def convert_notebook(path: Path) -> dict:
    nb = json.loads(path.read_text())
    cells = nb["cells"]
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        elif i > 0 and cells[i - 1]["cell_type"] == "code":
            text = "".join(cell["source"])
            stripped = PRINTED_OUTPUT.sub("", text, count=1)
            if stripped != text:
                cell["source"] = stripped.splitlines(keepends=True)
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir()

    for path in sorted((SRC / "notebooks").glob("*.ipynb")):
        nb = convert_notebook(path)
        (DST / path.name).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")

    for name in MD_PAGES:
        text = (SRC / "book" / name).read_text()
        if name == "ch17-docker-network.md":
            head, _, rest = text.partition("\n## 17.1")
            text = head.rstrip() + "\n" + CH17_NOTE + "\n## 17.1" + rest
        (DST / name).write_text(text)

    print(f"wrote {len(list(DST.iterdir()))} files to {DST}")


if __name__ == "__main__":
    main()
