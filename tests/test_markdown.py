from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from markdown_core import generate_readme, image_destination, make_table, save_markdown


class MarkdownTests(unittest.TestCase):
    def test_multiple_columns_and_rows(self):
        table = make_table("Name,Value", "Alice,10\nBob,20")
        self.assertEqual(table, "| Name | Value |\n| --- | --- |\n| Alice | 10 |\n| Bob | 20 |")

    def test_quoted_csv_commas_quotes_and_newlines(self):
        table = make_table("Name,Text", '"Alice, Jr.","A ""quote"""\nBob,"two\nlines"')
        self.assertIn('| Alice, Jr. | A "quote" |', table)
        self.assertIn("| Bob | two<br>lines |", table)

    def test_headerless_table_has_valid_gfm_structure(self):
        self.assertEqual(make_table("", "A,1", False), "|  |  |\n| --- | --- |\n| A | 1 |")

    def test_bad_table_shapes_fail_clearly(self):
        for headers, rows in [("A,B", "one"), ("A", "one,two"), ("A\nB", "one"), ("", "A,1"), ("A,B", '"unterminated')]:
            with self.subTest(headers=headers, rows=rows), self.assertRaises(ValueError):
                make_table(headers, rows)

    def test_pipe_backslash_and_html_cells(self):
        result = make_table("A", '"x|y <b> & \\path"')
        self.assertIn("x\\|y &lt;b&gt; &amp; \\\\path", result)

    def test_empty_optional_table(self):
        self.assertEqual(make_table("", ""), "")

    def test_multiline_code_and_embedded_fences(self):
        code = '    indented\n```\n````\nlast'
        result = generate_readme("Demo", code=code, language="python")
        self.assertIn("`````python\n" + code + "\n`````", result)

    def test_description_paragraphs_and_title_escaping(self):
        result = generate_readme("Demo [test]", "First paragraph.\n\nSecond paragraph.")
        self.assertIn("# Demo \\[test\\]", result)
        self.assertIn("First paragraph.\n\nSecond paragraph.", result)

    def test_image_paths_escape_spaces_and_parentheses(self):
        self.assertEqual(image_destination("images/my photo(1).png"), "images/my%20photo%281%29.png")
        self.assertIn("![A \\[preview\\]]", generate_readme("Demo", image_url="https://example.com/a.png", image_alt="A [preview]"))

    def test_invalid_image_urls_and_partial_input(self):
        for value in ("javascript:alert(1)", "data:image/png,abc", "https:/broken", "//example.com/a", "a\nb.png", "C:\\a.png"):
            with self.subTest(value=value), self.assertRaises(ValueError): image_destination(value)
        with self.assertRaises(ValueError): generate_readme("Demo", image_url="image.png")

    def test_required_title_and_invalid_language(self):
        with self.assertRaises(ValueError): generate_readme(" ")
        with self.assertRaises(ValueError): generate_readme("Demo", code="test", language="python\nmalformed")

    def test_utf8_atomic_save(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "README.md"
            content = generate_readme("Żółć", "Unicode: ąęć")
            save_markdown(path, content)
            self.assertEqual(path.read_text(encoding="utf-8"), content)
            self.assertEqual(list(Path(folder).glob("*.tmp")), [])

    def test_save_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "README.md"
            path.write_text("original", encoding="utf-8")
            with patch("markdown_core.os.replace", side_effect=PermissionError("read only")):
                with self.assertRaises(PermissionError): save_markdown(path, "new")
            self.assertEqual(path.read_text(encoding="utf-8"), "original")
            self.assertEqual(list(Path(folder).glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
