"""Small desktop README composer with CSV tables and safe UTF-8 export."""
import json
from pathlib import Path
import sys
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from ttkthemes import ThemedStyle
from markdown_core import generate_readme, save_markdown

VERSION = "1.1.0"


class ReadmeGenerator:
    def __init__(self, root):
        self.root = root
        root.title(f"README Generator {VERSION} — Swir")
        root.geometry("960x820")
        root.minsize(680, 540)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        style = ThemedStyle(root)
        try:
            style.set_theme("ubuntu")
        except tk.TclError:
            style.theme_use("clam")
        frame = ttk.Frame(root, padding=14)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(10, weight=1)
        self.title = tk.StringVar(root)
        self.headers = tk.StringVar(root)
        self.language = tk.StringVar(root)
        self.image_url = tk.StringVar(root)
        self.image_alt = tk.StringVar(root)
        self.include_table_header = tk.BooleanVar(root, True)
        self.status = tk.StringVar(root)
        self.title_entry = ttk.Entry(frame, textvariable=self.title)
        self.description_entry = scrolledtext.ScrolledText(frame, height=3, wrap="word")
        self.headers_entry = ttk.Entry(frame, textvariable=self.headers)
        self.data_entry = scrolledtext.ScrolledText(frame, height=4, wrap="none")
        self.code_entry = scrolledtext.ScrolledText(frame, height=4, wrap="none", font=("Consolas", 10))
        self.language_entry = ttk.Entry(frame, textvariable=self.language)
        self.image_url_entry = ttk.Entry(frame, textvariable=self.image_url)
        self.image_alt_entry = ttk.Entry(frame, textvariable=self.image_alt)
        controls = [("Project title:", self.title_entry), ("Description:", self.description_entry),
                    ("Headers (one CSV row):", self.headers_entry), ("Data (one CSV row per line):", self.data_entry),
                    ("Code example:", self.code_entry), ("Code language (optional):", self.language_entry),
                    ("Image URL or relative path:", self.image_url_entry), ("Image alternative text:", self.image_alt_entry)]
        for row, (label, widget) in enumerate(controls):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="nw", padx=(0, 12), pady=4)
            widget.grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Checkbutton(frame, text="Include table header labels", variable=self.include_table_header).grid(row=8, column=1, sticky="w", pady=4)
        buttons = ttk.Frame(frame)
        buttons.grid(row=9, column=0, columnspan=2, pady=8)
        self.generate_button = ttk.Button(buttons, text="Generate README", command=self.generate_readme)
        self.generate_button.pack(side="left", padx=4)
        ttk.Button(buttons, text="Preview Markdown", command=self.preview_readme).pack(side="left", padx=4)
        ttk.Button(buttons, text="Save README…", command=self.save_to_file).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear fields", command=self.clear_fields).pack(side="left", padx=4)
        self.generated_text = scrolledtext.ScrolledText(frame, height=10, wrap="none", font=("Consolas", 10), state="disabled")
        self.generated_text.grid(row=10, column=0, columnspan=2, sticky="nsew")
        horizontal = ttk.Scrollbar(frame, orient="horizontal", command=self.generated_text.xview)
        horizontal.grid(row=11, column=0, columnspan=2, sticky="ew")
        self.generated_text.configure(xscrollcommand=horizontal.set)
        ttk.Label(frame, textvariable=self.status, wraplength=850).grid(row=12, column=0, columnspan=2, sticky="ew", pady=(8, 0))

    def content(self):
        return generate_readme(self.title.get(), self.description_entry.get("1.0", "end-1c"), self.headers.get(),
                               self.data_entry.get("1.0", "end-1c"), self.code_entry.get("1.0", "end-1c"),
                               self.image_url.get(), self.image_alt.get(), self.include_table_header.get(), self.language.get())

    def display_readme(self, text):
        self.generated_text.configure(state="normal")
        self.generated_text.delete("1.0", "end")
        self.generated_text.insert("1.0", text)
        self.generated_text.configure(state="disabled")

    def generate_readme(self):
        try:
            content = self.content()
        except ValueError as error:
            self.status.set(str(error))
            self.display_readme("")
            return None
        self.display_readme(content)
        self.status.set("README generated.")
        return content

    def preview_readme(self):
        content = self.generate_readme()
        if content is None:
            return
        window = tk.Toplevel(self.root)
        window.title("README Markdown preview")
        output = scrolledtext.ScrolledText(window, wrap="word", font=("Consolas", 10), width=90, height=30)
        output.insert("1.0", content)
        output.configure(state="disabled")
        output.pack(expand=True, fill="both")

    def save_to_file(self, path=None):
        content = self.generate_readme()
        if content is None:
            return False
        if path is None:
            path = filedialog.asksaveasfilename(parent=self.root, defaultextension=".md", initialfile="README.md", filetypes=[("Markdown files", "*.md")])
        if not path:
            self.status.set("Save cancelled.")
            return False
        try:
            save_markdown(path, content)
        except OSError as error:
            self.status.set(f"Could not save README: {error}")
            return False
        self.status.set(f"Saved: {path}")
        return True

    def clear_fields(self):
        for variable in (self.title, self.headers, self.language, self.image_url, self.image_alt):
            variable.set("")
        for widget in (self.description_entry, self.data_entry, self.code_entry):
            widget.delete("1.0", "end")
        self.include_table_header.set(True)
        self.display_readme("")
        self.status.set("")


def self_test(report):
    root = None
    result = {"application":"GitHub-README-Generator", "version":VERSION, "passed":False}
    try:
        parent = Path(report).resolve().parent
        with tempfile.TemporaryDirectory(prefix="readme-smoke-", dir=parent) as folder:
            if not Path(folder).resolve().is_relative_to(parent):
                raise RuntimeError("Unexpected smoke-test directory")
            root = tk.Tk()
            root.withdraw()
            app = ReadmeGenerator(root)
            root.update_idletasks()
            app.title.set("Demo")
            app.headers.set("Name,Value")
            app.data_entry.insert("1.0", '"Alice, Jr.",10\nBob,20')
            app.code_entry.insert("1.0", 'print("Hello")\nprint("World")')
            app.language.set("python")
            app.generate_button.invoke()
            content = app.generated_text.get("1.0", "end-1c")
            assert "| Alice, Jr. | 10 |" in content and "| Bob | 20 |" in content and "```python" in content
            destination = Path(folder) / "README.md"
            assert app.save_to_file(destination)
            assert destination.read_text(encoding="utf-8") == content
            app.headers.set("OnlyOne")
            assert app.generate_readme() is None
            app.clear_fields()
            assert not app.title.get() and not app.generated_text.get("1.0", "end-1c")
            root.destroy()
            root = None
            result.update(passed=True, checks=["Tk and theme", "CSV table generation", "multiline code", "UTF-8 export", "invalid columns", "clear fields"])
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
    finally:
        if root is not None:
            root.destroy()
        Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result["passed"] else 1


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--self-test":
        return self_test(sys.argv[2])
    root = tk.Tk()
    ReadmeGenerator(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
