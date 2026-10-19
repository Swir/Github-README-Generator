"""CSV-aware Markdown generation and atomic UTF-8 saving."""
import csv
import html
import io
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote, urlsplit


def escape_inline(text):
    return re.sub(r"([\\`*_{}\[\]()#+.!|>\-])", r"\\\1", " ".join(text.splitlines()))


def csv_rows(text):
    if len(text) > 128 * 1024:
        raise ValueError("Table input is too large (maximum 128 KiB).")
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), skipinitialspace=True, strict=True))
    except csv.Error as error:
        raise ValueError(f"Invalid CSV: {error}") from error
    rows = [row for row in rows if any(cell.strip() for cell in row)]
    if len(rows) > 1000 or any(len(row) > 50 for row in rows):
        raise ValueError("Tables support up to 1,000 rows and 50 columns.")
    return rows


def table_cell(text):
    return html.escape(text.strip(), quote=False).replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def make_table(headers_text, data_text, include_header=True):
    if not headers_text.strip() and not data_text.strip():
        return ""
    headers = csv_rows(headers_text)
    if len(headers) > 1:
        raise ValueError("Table headers must be a single CSV row.")
    rows = csv_rows(data_text)
    header = headers[0] if headers else []
    if include_header and not header:
        raise ValueError("Enter column headers or turn off header labels.")
    count = len(header) if header else (len(rows[0]) if rows else 0)
    if not count:
        return ""
    for index, row in enumerate(rows, start=1):
        if len(row) != count:
            raise ValueError(f"Table row {index} has {len(row)} columns; expected {count}.")
    if not include_header:
        header = [""] * count
    lines = ["| " + " | ".join(table_cell(cell) for cell in header) + " |", "| " + " | ".join("---" for _ in range(count)) + " |"]
    lines.extend("| " + " | ".join(table_cell(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def image_destination(value):
    value = value.strip()
    if not value or any(ord(char) < 32 for char in value):
        raise ValueError("Enter an image URL or relative path without control characters.")
    parsed = urlsplit(value)
    if parsed.scheme and parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Images support HTTP(S) URLs or relative repository paths.")
    if parsed.scheme and not parsed.netloc:
        raise ValueError("The image URL needs a hostname.")
    if value.startswith("//") or "\\" in value:
        raise ValueError("Use an explicit HTTP(S) URL or a relative path with forward slashes.")
    return quote(value, safe="/:#?&=%+@~._-")


def generate_readme(title, description="", headers="", data="", code="", image_url="", image_alt="", include_header=True, language=""):
    title = title.strip()
    if not title:
        raise ValueError("Enter a project title.")
    if len(title) > 200:
        raise ValueError("The title is limited to 200 characters.")
    if not re.fullmatch(r"[A-Za-z0-9_+.#-]{0,32}", language.strip()):
        raise ValueError("Use a short code-language name, for example python, javascript or c++.")
    parts = ["# " + escape_inline(title)]
    if description.strip():
        parts.append(description.strip())
    table = make_table(headers, data, include_header)
    if table:
        parts.append("## Table\n\n" + table)
    if code.strip():
        longest = max((len(match.group()) for match in re.finditer(r"`+", code)), default=0)
        fence = "`" * max(3, longest + 1)
        parts.append(f"## Code Example\n\n{fence}{language.strip()}\n{code.rstrip(chr(10))}\n{fence}")
    if image_url.strip() or image_alt.strip():
        if not image_url.strip() or not image_alt.strip():
            raise ValueError("Provide both an image URL/path and alternative text.")
        parts.append(f"## Image\n\n![{escape_inline(image_alt.strip())}]({image_destination(image_url)})")
    return "\n\n".join(parts) + "\n"


def save_markdown(path, content):
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=".readme-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
