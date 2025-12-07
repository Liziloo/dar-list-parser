# pdf_to_text.py
import sys
import re
from pathlib import Path

import fitz  # PyMuPDF

HEADER_PATTERN = re.compile(r"^[A-Z][a-z]+ \d+$")  # e.g. "Maine 23"


def extract_text(
    pdf_path: Path,
    pages: str | None = None,
    remove_headers: bool = True,
    merge_hyphens: bool = True,
) -> str:
    doc = fitz.open(pdf_path)
    page_indices: list[int]

    if pages:
        # pages string like "36-43" or "10,12,15-17"
        indices: list[int] = []
        for part in pages.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-", 1)
                for p in range(int(start), int(end) + 1):
                    indices.append(p - 1)  # 1-based to 0-based
            else:
                indices.append(int(part) - 1)
        page_indices = [i for i in indices if 0 <= i < len(doc)]
    else:
        page_indices = list(range(len(doc)))

    lines: list[str] = []
    for i in page_indices:
        text = doc.load_page(i).get_text("text")
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            if remove_headers and HEADER_PATTERN.match(line.strip()):
                continue
            lines.append(line)

    full_text = "\n".join(lines)

    if merge_hyphens:
        # Merge words split at line breaks, e.g. "Passamaquod-\n dy"
        full_text = re.sub(r"-\n(\S)", r"\1", full_text)
        # Normalize remaining newlines to spaces where appropriate
        full_text = re.sub(r"\n+", "\n", full_text)

    return full_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_text.py input.pdf [pages]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    pages = sys.argv[2] if len(sys.argv) >= 3 else None

    text = extract_text(pdf_path, pages=pages)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
