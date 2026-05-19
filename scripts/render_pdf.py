#!/usr/bin/env python3
"""
render_pdf.py — Convert a resume Markdown file to an ATS-friendly PDF.

Usage:
    python render_pdf.py input.md output.pdf [--lang zh-Hant|en] [--title "Resume"]

The output is a single-column, real-text PDF with CJK font support (Noto Sans CJK
or DejaVu fallback). Designed to text-extract cleanly through ATS parsers.

Dependencies:
    pip install markdown weasyprint
    System fonts: 'fonts-noto-cjk' (Linux) or any CJK font available to fontconfig.

If WeasyPrint cannot be installed (no system Cairo / Pango), fall back to using
the docx skill: Markdown → DOCX → PDF.
"""

import argparse
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Missing dependency: pip install markdown", file=sys.stderr)
    sys.exit(1)


# CSS template: single-column, ATS-friendly, CJK-capable.
CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 14mm 14mm 14mm 14mm;
}

html, body {
    font-family: "Noto Sans CJK TC", "Noto Sans TC", "PingFang TC",
                 "Microsoft JhengHei", "Helvetica Neue", Helvetica, Arial,
                 "DejaVu Sans", sans-serif;
    font-size: 10.5pt;
    line-height: 1.4;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

h1 {
    font-size: 20pt;
    font-weight: 700;
    margin: 0 0 2pt 0;
    color: #111;
    letter-spacing: 0.2pt;
}

.headline {
    font-size: 10.5pt;
    color: #555;
    margin: 0 0 6pt 0;
}

.contact {
    font-size: 9.5pt;
    color: #444;
    margin: 0 0 10pt 0;
}

h2 {
    font-size: 12pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    color: #111;
    border-bottom: 1pt solid #333;
    padding-bottom: 2pt;
    margin: 12pt 0 6pt 0;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    margin: 8pt 0 2pt 0;
    color: #111;
}

h3 + p em,
h3 em {
    color: #555;
    font-style: normal;
    font-size: 10pt;
}

p {
    margin: 2pt 0;
}

ul {
    margin: 4pt 0 6pt 0;
    padding-left: 16pt;
}

li {
    margin: 1pt 0;
}

strong {
    font-weight: 700;
}

a {
    color: #1a1a1a;
    text-decoration: none;
}

hr {
    border: none;
    border-top: 0.5pt solid #ccc;
    margin: 4pt 0;
}

.role-header {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
}

.dates {
    color: #555;
    font-weight: 400;
    white-space: nowrap;
}
"""


HTML_WRAPPER = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_text: str) -> str:
    """Convert Markdown to HTML with common extensions."""
    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])
    return md.convert(md_text)


def render_pdf(input_md: Path, output_pdf: Path, lang: str, title: str) -> None:
    md_text = input_md.read_text(encoding="utf-8")
    body_html = md_to_html(md_text)
    full_html = HTML_WRAPPER.format(
        lang=lang, title=title, css=CSS_TEMPLATE, body=body_html
    )

    # Try WeasyPrint first.
    try:
        from weasyprint import HTML

        HTML(string=full_html).write_pdf(str(output_pdf))
        print(f"Wrote PDF via WeasyPrint: {output_pdf}")
        return
    except ImportError:
        print("WeasyPrint not installed; trying playwright fallback...", file=sys.stderr)
    except Exception as exc:
        print(f"WeasyPrint failed ({exc}); trying playwright fallback...", file=sys.stderr)

    # Fallback: playwright (headless Chromium prints to PDF).
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(full_html, wait_until="domcontentloaded")
            page.pdf(
                path=str(output_pdf),
                format="A4",
                margin={"top": "14mm", "right": "14mm", "bottom": "14mm", "left": "14mm"},
                print_background=True,
            )
            browser.close()
        print(f"Wrote PDF via Playwright: {output_pdf}")
        return
    except ImportError:
        print(
            "Playwright not installed either.\n"
            "Install one of:\n"
            "  pip install weasyprint    # plus system Cairo/Pango libs\n"
            "  pip install playwright && playwright install chromium\n"
            "\n"
            "Or use the docx skill to render: Markdown → DOCX → PDF.",
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception as exc:
        print(f"Playwright also failed: {exc}", file=sys.stderr)
        sys.exit(3)


def main():
    parser = argparse.ArgumentParser(
        description="Render a resume Markdown file to an ATS-friendly PDF."
    )
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--lang",
        default="zh-Hant",
        choices=["zh-Hant", "en"],
        help="Resume language (affects HTML lang attribute and font hinting)",
    )
    parser.add_argument(
        "--title", default="Resume", help="PDF title metadata (shows in viewers)"
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(args.input, args.output, args.lang, args.title)


if __name__ == "__main__":
    main()
