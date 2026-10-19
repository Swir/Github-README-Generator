# Changelog

## 1.1.0 — 2026-10-19

- Fix CSV table parsing: support multiple rows, quoted commas, escaped quotes and multiline cells.
- Validate column counts and retain valid GitHub Markdown structure when header labels are hidden.
- Escape table pipes/HTML, image paths and alternative text; safely fence code containing backticks.
- Add multiline description/code/table inputs and an optional code-language field.
- Preserve paragraph breaks and code indentation.
- Save UTF-8 files atomically and report export failures without losing the existing file.
- Add regression tests and a frozen-runtime test covering real table generation, theme resources and file export before release.
