import unittest

from textnode import TextNode, TextType
import utils as utils

from utils import paragraph, heading, code, quote, unordered_list, ordered_list


class TestTextNodeToLeafNode(unittest.TestCase):
    def test_normal(self):
        text = TextNode("normal", TextType.NORMAL)
        node = utils.text_node_to_html_node(text)
        self.assertEqual(node.to_html(), "normal")

    def test_bold(self):
        text = TextNode("bold", TextType.BOLD)
        node = utils.text_node_to_html_node(text)
        self.assertEqual(node.to_html(), "<b>bold</b>")

    def test_italic(self):
        text = TextNode("italic", TextType.ITALIC)
        node = utils.text_node_to_html_node(text)
        self.assertEqual(node.to_html(), "<i>italic</i>")

    def test_code(self):
        text = TextNode("code", TextType.CODE)
        node = utils.text_node_to_html_node(text)
        self.assertEqual(node.to_html(), "<code>code</code>")

    def test_link(self):
        text = TextNode("link", TextType.LINK, 'link.co')
        node = utils.text_node_to_html_node(text)
        self.assertEqual(node.to_html(), "<a href=\"link.co\">link</a>")

    def test_image(self):
        text = TextNode("image", TextType.IMAGE, 'link.co')
        node = utils.text_node_to_html_node(text)
        self.assertEqual(
            node.to_html(), "<img src=\"link.co\" alt=\"image\"></img>")


class TestTextToTextNodes(unittest.TestCase):
    def test_no_markdown(self):
        result = utils.text_to_textnodes('no markdown here!')
        self.assertEqual(
            result, [TextNode('no markdown here!', TextType.NORMAL)])

    def test_just_bold(self):
        result = utils.text_to_textnodes('just **bold** markdown')
        expected = [
            TextNode('just ', TextType.NORMAL),
            TextNode('bold', TextType.BOLD),
            TextNode(' markdown', TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_just_italic(self):
        result = utils.text_to_textnodes('just *italic* markdown')
        expected = [
            TextNode('just ', TextType.NORMAL),
            TextNode('italic', TextType.ITALIC),
            TextNode(' markdown', TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_bold_and_italic(self):
        result = utils.text_to_textnodes('**bold** and *italic* markdown')
        expected = [
            TextNode('bold', TextType.BOLD),
            TextNode(' and ', TextType.NORMAL),
            TextNode('italic', TextType.ITALIC),
            TextNode(' markdown', TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_just_code(self):
        result = utils.text_to_textnodes('just `code` markdown')
        expected = [
            TextNode('just ', TextType.NORMAL),
            TextNode('code', TextType.CODE),
            TextNode(' markdown', TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_bold_italic_and_code(self):
        result = utils.text_to_textnodes(
            '**bold** and *italic* markdown with `code`')
        expected = [
            TextNode('bold', TextType.BOLD),
            TextNode(' and ', TextType.NORMAL),
            TextNode('italic', TextType.ITALIC),
            TextNode(' markdown with ', TextType.NORMAL),
            TextNode('code', TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_bold_italic_code_and_image(self):
        result = utils.text_to_textnodes(
            '**bold** and *italic* markdown with `code` and an ![image](image.url)')
        expected = [
            TextNode('bold', TextType.BOLD),
            TextNode(' and ', TextType.NORMAL),
            TextNode('italic', TextType.ITALIC),
            TextNode(' markdown with ', TextType.NORMAL),
            TextNode('code', TextType.CODE),
            TextNode(' and an ', TextType.NORMAL),
            TextNode('image', TextType.IMAGE, "image.url"),
        ]
        self.assertEqual(result, expected)

    def test_all(self):
        result = utils.text_to_textnodes(
            'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```
This is a code block
```
            """
        blocks = utils.markdown_to_blocks(text)
        self.assertEqual(blocks, [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item',
            '```\nThis is a code block\n```'
        ])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_types(self):
        block = "# heading"
        self.assertEqual(utils.block_to_block_type(block), heading + "1")
        block = "### heading"
        self.assertEqual(utils.block_to_block_type(block), heading + "3")
        block = "```\ncode\n```"
        self.assertEqual(utils.block_to_block_type(block), code)
        block = "> quote\n> more quote"
        self.assertEqual(utils.block_to_block_type(block), quote)
        block = "* list\n* items"
        self.assertEqual(utils.block_to_block_type(block), unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(utils.block_to_block_type(block), ordered_list)
        block = "paragraph"
        self.assertEqual(utils.block_to_block_type(block), paragraph)


class TestGetBlockLines(unittest.TestCase):
    def test_get_heading_lines(self):
        lines = utils.get_block_lines("# heading", "heading")
        self.assertEqual(lines, ["heading"])
        lines2 = utils.get_block_lines("#### heading2", "heading")
        self.assertEqual(lines2, ["heading2"])

    def test_get_code_line(self):
        lines = utils.get_block_lines("```\ncode\n```", "code")
        self.assertEqual(lines, ["code"])

    def test_get_quote_line(self):
        lines = utils.get_block_lines("> quote", "quote")
        self.assertEqual(lines, ["quote"])

    def test_get_unordered_list(self):
        lines = utils.get_block_lines("* list item", "unordered_list")
        self.assertEqual(lines, ["list item"])
        lines2 = utils.get_block_lines("- list item 2", "unordered_list")
        self.assertEqual(lines2, ["list item 2"])

    def test_get_ordered_list(self):
        lines = utils.get_block_lines(
            "1. list item\n2. list item 2", "ordered_list")
        self.assertEqual(lines, ["list item", "list item 2"])

    def test_no_block_type(self):
        lines = utils.get_block_lines("line1\nline2")
        self.assertEqual(lines, ["line1", "line2"])
