import unittest

from generator_utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_success(self):
        markdown = "# Title\nSome more text"
        title = extract_title(markdown)
        self.assertEqual(title, "Title")

    def test_multiword_title(self):
        markdown = "# Another Title\njust a paragraph"
        title = extract_title(markdown)
        self.assertEqual(title, "Another Title")

    def test_no_header_one(self):
        markdown = "## Header two\nwrong header!"
        with self.assertRaises(Exception) as e:
            extract_title(markdown)
        self.assertEqual(str(e.exception), "No title found!")
