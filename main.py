import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import textwrap
from ttkthemes import ThemedStyle

class ReadmeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Readme Generator by Swir 1.0")

        self.create_widgets()

    def create_widgets(self):
        style = ThemedStyle(self.root)
        style.set_theme("ubuntu")

        self.title_label = ttk.Label(self.root, text="Title:")
        self.title_entry = ttk.Entry(self.root, width=30)

        self.description_label = ttk.Label(self.root, text="Description:")
        self.description_entry = ttk.Entry(self.root, width=30)

        self.headers_label = ttk.Label(self.root, text="Table Headers (comma-separated):")
        self.headers_entry = ttk.Entry(self.root, width=30)

        self.data_label = ttk.Label(self.root, text="Table Data (rows, comma-separated):")
        self.data_entry = ttk.Entry(self.root, width=30)

        self.code_label = ttk.Label(self.root, text="Code Example:")
        self.code_entry = ttk.Entry(self.root, width=30)

        self.image_url_label = ttk.Label(self.root, text="Image URL:")
        self.image_url_entry = ttk.Entry(self.root, width=30)

        self.image_alt_label = ttk.Label(self.root, text="Image Alt Text:")
        self.image_alt_entry = ttk.Entry(self.root, width=30)

        self.include_table_header = tk.BooleanVar()
        self.include_table_header.set(True)
        self.include_table_header_checkbox = ttk.Checkbutton(self.root, text="Include Table Header", variable=self.include_table_header)

        self.generated_text = scrolledtext.ScrolledText(self.root, wrap="none", bg="#f0f0f0", fg="black", font=("Arial", 10))
        self.generated_text.config(state="disabled", height=20, width=80)

        self.preview_button = ttk.Button(self.root, text="Preview README", command=self.preview_readme)
        self.generate_button = ttk.Button(self.root, text="Generate README", command=self.generate_readme)
        self.clear_button = ttk.Button(self.root, text="Clear Fields", command=self.clear_fields)
        self.save_button = ttk.Button(self.root, text="Save README to File", command=self.save_to_file)

        # Layout
        rows = 0
        for widget in (self.title_label, self.title_entry, self.description_label, self.description_entry,
                       self.headers_label, self.headers_entry, self.data_label, self.data_entry,
                       self.code_label, self.code_entry, self.image_url_label, self.image_url_entry,
                       self.image_alt_label, self.image_alt_entry, self.include_table_header_checkbox,
                       self.generated_text, self.preview_button, self.generate_button, self.clear_button, self.save_button):
            widget.grid(row=rows // 2, column=rows % 2, sticky="w", pady=(10, 0))
            rows += 1

    def generate_readme(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        headers = [header.strip() for header in self.headers_entry.get().split(',')]
        data = [row.strip().split(',') for row in self.data_entry.get().split(',')]
        code_example = self.code_entry.get().strip()
        image_url = self.image_url_entry.get().strip()
        image_alt_text = self.image_alt_entry.get().strip()

        readme_text = self.generate_readme_content(title, description, headers, data, code_example, image_url, image_alt_text)

        self.display_readme(readme_text)

    def generate_readme_content(self, title, description, headers, data, code_example, image_url, image_alt_text):
        content = []

        if title:
            content.append(f"# {title}\n\n")

        if description:
            content.append(f"{textwrap.fill(description, width=80)}\n\n")

        if headers and any(data_row for data_row in data if any(field.strip() for field in data_row)):
            header_row = ' | '.join(headers) if self.include_table_header.get() else ''
            separator = '|'.join(['---' for _ in headers])
            table_content = f"{header_row}\n{separator}\n"
            table_content += '\n'.join([' | '.join(row) for row in data if any(field.strip() for field in row)])
            content.append(f"## Table\n{table_content}\n")

        if code_example:
            content.append(f"## Code Example\n```\n{code_example}\n```\n")

        if image_url and image_alt_text:
            content.append(f"## Image\n![{image_alt_text}]({image_url})\n")

        return ''.join(content)

    def display_readme(self, readme_text):
        self.generated_text.config(state="normal")
        self.generated_text.delete(1.0, tk.END)
        self.generated_text.insert(tk.END, readme_text)
        self.generated_text.config(state="disabled")

    def clear_fields(self):
        for entry in [self.title_entry, self.description_entry, self.headers_entry, self.data_entry,
                      self.code_entry, self.image_url_entry, self.image_alt_entry]:
            entry.delete(0, tk.END)

        self.include_table_header.set(True)
        self.generated_text.config(state="normal")
        self.generated_text.delete(1.0, tk.END)
        self.generated_text.config(state="disabled")

    def save_to_file(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title must be filled before saving to file.")
            return

        readme_text = self.generate_readme_content(
            title,
            self.description_entry.get().strip(),
            [header.strip() for header in self.headers_entry.get().split(',')],
            [row.strip().split(',') for row in self.data_entry.get().split(',')],
            self.code_entry.get().strip(),
            self.image_url_entry.get().strip(),
            self.image_alt_entry.get().strip()
        )

        file_path = self.ask_for_file_path()
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(readme_text)

            messagebox.showinfo("Success", f"README saved to {file_path}")

    def ask_for_file_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        return file_path if file_path else None

    def preview_readme(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        headers = [header.strip() for header in self.headers_entry.get().split(',')]
        data = [row.strip().split(',') for row in self.data_entry.get().split(',')]
        code_example = self.code_entry.get().strip()
        image_url = self.image_url_entry.get().strip()
        image_alt_text = self.image_alt_entry.get().strip()

        readme_text = self.generate_readme_content(title, description, headers, data, code_example, image_url, image_alt_text)

        preview_window = tk.Toplevel(self.root)
        preview_window.title("Preview README")

        preview_text = scrolledtext.ScrolledText(preview_window, wrap="none", bg="#f0f0f0", fg="black", font=("Arial", 10))
        preview_text.insert(tk.END, readme_text)
        preview_text.config(state="disabled", height=20, width=80)
        preview_text.pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReadmeGenerator(root)
    root.mainloop()
