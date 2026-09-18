<!-- SWIR-README-STANDARD:v2 -->

<div align="center">

<img width="100%" src="assets/readme/hero.svg" alt="GitHub README Generator — desktop Markdown README builder" />

<br>

![Python](https://img.shields.io/badge/Python-3.11-02050A?style=for-the-badge&logo=python&logoColor=62E5FF)
![GUI](https://img.shields.io/badge/GUI-Tkinter-02050A?style=for-the-badge&logo=python&logoColor=62E5FF)
![Output](https://img.shields.io/badge/Output-Markdown-02050A?style=for-the-badge&logo=markdown&logoColor=62E5FF)
![Release](https://img.shields.io/badge/Release-v1.0.0-02050A?style=for-the-badge&logo=github&logoColor=62E5FF)

[![Author](https://img.shields.io/badge/Author-Swir-0088FF?style=flat-square&logo=github)](https://github.com/Swir)
[![Stars](https://img.shields.io/github/stars/Swir/Github-README-Generator?style=flat-square&color=0088FF)](https://github.com/Swir/Github-README-Generator/stargazers)

</div>

GitHub README Generator is a lightweight desktop utility for composing simple Markdown README files without manually typing every Markdown structure.

## 📍 Project Status

<img width="100%" src="assets/readme/progress-card.svg" alt="GitHub README Generator product progress — N/A because no authoritative roadmap exists" />

**Product progress:** **N/A** — this legacy utility has no authoritative, measurable product roadmap. The published release is not treated as a completion percentage.

| Item | Status |
|---|---|
| Current stage | Released utility |
| Primary UI | Tkinter + `ttkthemes` |
| Verified release workflow runtime | Python 3.11 on Windows |
| Latest public release | [v1.0.0](https://github.com/Swir/Github-README-Generator/releases/tag/v1.0.0) |
| Product roadmap | Not present |

## 🚀 Overview

The application collects a project title, description, optional Markdown table, code example and image metadata, then generates a Markdown document that can be previewed in the GUI and saved as a `.md` file. The current implementation is intentionally small and direct; it is a README drafting utility rather than a full Markdown IDE.

## ✨ Highlights

| Feature | What it does |
|---|---|
| 🏷️ Project title and description | Creates the main heading and wrapped overview text |
| 📊 Table builder | Builds Markdown tables from comma-separated headers and row data |
| 🧾 Optional table header | Lets the generated table omit the header row when desired |
| 💻 Code section | Adds a fenced code example section |
| 🖼️ Image block | Generates Markdown image syntax from a URL and alternative text |
| 👁️ Preview | Opens the generated Markdown in a read-only preview window |
| 💾 Save | Writes the generated README to a user-selected `.md` file |
| 🧹 Clear | Resets form fields and generated output |
| 🐧 Ubuntu theme | Uses the `ttkthemes` Ubuntu theme for the desktop interface |

## ⚙️ Quick Start

### Recommended Windows build

Download the real **v1.0.0** release. It contains the Windows EXE, a portable Windows x64 ZIP and a SHA-256 file for that ZIP.

[**Open GitHub Releases →**](https://github.com/Swir/Github-README-Generator/releases)

### From source

```bash
git clone https://github.com/Swir/Github-README-Generator.git
cd Github-README-Generator
python -m pip install ttkthemes
python main.py
```

The repository release workflow validates `main.py` with Python 3.11 and builds the Windows executable with PyInstaller. The source itself has no declared cross-platform CI matrix, so broader runtime support is not claimed here.

## 🎮 Usage

1. Enter a project title and optional description.
2. Add comma-separated table headers and row data if needed.
3. Add a code example and/or image URL plus alt text.
4. Choose whether a table header should be included.
5. Use **Preview README** to inspect the generated Markdown.
6. Use **Generate README** to refresh the main output.
7. Use **Save README to File** to write the result to disk.

## 🧠 Implementation

| Layer | Technology / role |
|---|---|
| Desktop UI | Python `tkinter` / `ttk` |
| Theme | `ttkthemes` (`ubuntu`) |
| Markdown generation | Python string assembly + `textwrap` |
| Preview | Tkinter `Toplevel` + read-only `ScrolledText` |
| Windows packaging | PyInstaller in the repository release workflow |

## 🗺️ Roadmap / Progress

<img width="100%" src="assets/readme/progress-mini.svg" alt="GitHub README Generator compact product progress — N/A" />

**Measured scope:** product roadmap · **Progress:** N/A · **Counter:** N/A — no canonical checklist or weighted roadmap exists.

The SVG deliberately shows **N/A** instead of inventing a completion percentage from the v1.0.0 release, commit count or documentation state.

## 📦 Releases

The latest verified public release is **v1.0.0**. The release workflow validates the Python source, builds a one-file windowed EXE, packages a portable ZIP and writes a SHA-256 file for the ZIP.

[**GitHub Releases →**](https://github.com/Swir/Github-README-Generator/releases)

## ⚠️ Limitations

- The table input uses a simple comma-separated format rather than a full structured editor.
- The generated code block does not assign a syntax language.
- Image support inserts Markdown links; it does not upload or manage image files.
- The preview is plain text, not a rendered GitHub Markdown browser.
- No authoritative roadmap exists, so product completion is intentionally reported as N/A.

## 🔎 Search Keywords

`github readme generator` • `markdown readme builder` • `python markdown gui` • `tkinter readme generator` • `desktop markdown tool` • `markdown table generator` • `github documentation utility` • `readme preview tool` • `python tkinter utility` • `windows readme generator` • `markdown image syntax` • `markdown code block generator`

<div align="center">

<img src="assets/readme/icon.svg" width="96" alt="GitHub README Generator icon" />

### `WRITE • PREVIEW • SAVE • DOCUMENT`

⭐ **If this utility is useful, consider leaving a star.**

[**← SWIR profile**](https://github.com/Swir) · [**All projects →**](https://github.com/Swir?tab=repositories)

</div>
