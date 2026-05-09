#!/usr/bin/env python3
"""Render the initial white paper Markdown into a simple PDF.

This renderer intentionally uses only the Python standard library so the
repository can produce a citable PDF artifact without requiring Pandoc or LaTeX.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "initial-white-paper.md"
TARGET = ROOT / "reports" / "initial-white-paper.pdf"

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN = 54
LINE_HEIGHT = 14
TITLE_SIZE = 18
BODY_SIZE = 10
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def normalize_markdown_line(line: str) -> tuple[str, bool]:
    stripped = line.strip()
    if not stripped:
        return "", False
    if stripped.startswith("#"):
        return stripped.lstrip("#").strip(), True
    if stripped.startswith("|"):
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r"-+", cell.replace(" ", "")) for cell in cells):
            return "", False
        return " | ".join(cells), False
    if stripped.startswith("- "):
        return f"- {stripped[2:].strip()}", False
    if re.match(r"^\d+\. ", stripped):
        return stripped, False
    return stripped, False


def build_lines(markdown: str) -> list[tuple[str, bool]]:
    output: list[tuple[str, bool]] = []
    for raw_line in markdown.splitlines():
        line, is_heading = normalize_markdown_line(raw_line)
        if not line:
            output.append(("", False))
            continue
        width = 68 if is_heading else 92
        for wrapped in textwrap.wrap(line, width=width, replace_whitespace=False):
            output.append((wrapped, is_heading))
        if is_heading:
            output.append(("", False))
    return output


def page_stream(lines: list[tuple[str, bool]]) -> str:
    commands = ["BT"]
    y = PAGE_HEIGHT - MARGIN
    for text, is_heading in lines:
        if y < MARGIN:
            break
        if not text:
            y -= LINE_HEIGHT
            continue
        font = "F2" if is_heading else "F1"
        size = TITLE_SIZE if is_heading else BODY_SIZE
        commands.append(f"/{font} {size} Tf")
        commands.append(f"1 0 0 1 {MARGIN} {y} Tm")
        commands.append(f"({escape_pdf_text(text)}) Tj")
        y -= LINE_HEIGHT + (5 if is_heading else 0)
    commands.append("ET")
    return "\n".join(commands)


def chunk_pages(lines: list[tuple[str, bool]]) -> list[list[tuple[str, bool]]]:
    pages: list[list[tuple[str, bool]]] = []
    current: list[tuple[str, bool]] = []
    y = PAGE_HEIGHT - MARGIN
    for line in lines:
        _, is_heading = line
        needed = LINE_HEIGHT + (5 if is_heading else 0)
        if y - needed < MARGIN and current:
            pages.append(current)
            current = []
            y = PAGE_HEIGHT - MARGIN
        current.append(line)
        y -= needed
    if current:
        pages.append(current)
    return pages


def render_pdf(markdown: str) -> bytes:
    lines = build_lines(markdown)
    pages = chunk_pages(lines)

    objects: list[str] = []
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")

    page_refs = " ".join(f"{5 + index * 2} 0 R" for index in range(len(pages)))
    objects.append(f"<< /Type /Pages /Kids [{page_refs}] /Count {len(pages)} >>")
    objects.append(f"<< /Type /Font /Subtype /Type1 /BaseFont /{FONT} >>")
    objects.append(f"<< /Type /Font /Subtype /Type1 /BaseFont /{FONT_BOLD} >>")

    for index, page_lines in enumerate(pages):
        page_object_id = 5 + index * 2
        content_object_id = page_object_id + 1
        objects.append(
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_object_id} 0 R >>"
        )
        stream = page_stream(page_lines)
        objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")

    pdf = "%PDF-1.4\n"
    offsets = [0]
    for object_id, body in enumerate(objects, start=1):
        offsets.append(len(pdf.encode("latin-1")))
        pdf += f"{object_id} 0 obj\n{body}\nendobj\n"

    xref_offset = len(pdf.encode("latin-1"))
    pdf += f"xref\n0 {len(objects) + 1}\n"
    pdf += "0000000000 65535 f \n"
    for offset in offsets[1:]:
        pdf += f"{offset:010d} 00000 n \n"
    pdf += "trailer\n"
    pdf += f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
    pdf += "startxref\n"
    pdf += f"{xref_offset}\n"
    pdf += "%%EOF\n"
    return pdf.encode("latin-1")


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    TARGET.write_bytes(render_pdf(markdown))
    print(f"Wrote {TARGET}")


if __name__ == "__main__":
    main()
