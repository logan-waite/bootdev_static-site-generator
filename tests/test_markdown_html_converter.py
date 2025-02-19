import unittest

from markdown_html_converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is just a normal paragraph"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, "<div><p>This is just a normal paragraph</p></div>")

    def test_multiple_paragraphs(self):
        markdown = \
            """This is the first paragraph

            This is the second paragraph"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, "<div><p>This is the first paragraph</p><p>This is the second paragraph</p></div>")

    def test_bold_text(self):
        markdown = "This is **bold** text"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bold</b> text</p></div>")

    def test_italic_text(self):
        markdown = "This is *italic* text"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <i>italic</i> text</p></div>")

    def test_code_block(self):
        markdown = """
```
This is a code block
```
            """
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><code>This is a code block</code></div>")

    def test_unordered_list_block(self):
        markdown = """
* First item
* Second item
* Third item
            """
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>")
        markdown2 = """
- First item
- Second item
- Third item
            """
        node2 = markdown_to_html_node(markdown2)
        html2 = node2.to_html()
        self.assertEqual(
            html2, "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>")

    def test_unordered_list_with_italics(self):
        markdown = """
* First item
* Second item *is italicized*
* Third item
        """
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>First item</li><li>Second item <i>is italicized</i></li><li>Third item</li></ul></div>")

    def test_ordered_list_block(self):
        markdown = """
1. First item
2. Second item
3. Third item
            """
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>")

    def test_heading_block(self):
        markdown = "# heading 1"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>heading 1</h1></div>")

        markdown2 = "### heading 3"
        node2 = markdown_to_html_node(markdown2)
        html2 = node2.to_html()
        self.assertEqual(html2, "<div><h3>heading 3</h3></div>")

    def test_all_together(self):
        markdown = """ 
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. order list one
2. ordered list two
3. ordered list the third

```
    this is a code block
```

- another unordered list
- doing it again

do some `code` just for kicks and giggles
            """
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><ol><li>order list one</li><li>ordered list two</li><li>ordered list the third</li></ol><code>this is a code block</code><ul><li>another unordered list</li><li>doing it again</li></ul><p>do some <code>code</code> just for kicks and giggles</p></div>")
