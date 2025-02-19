import unittest

from splitters import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_split(self):
        text = TextNode("this text has no delimiters", TextType.NORMAL)
        result = split_nodes_delimiter([text], "**", TextType.BOLD)
        self.assertEqual(result[0], text)

    def test_italic_split(self):
        text = TextNode("this text has *italic* text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(result[2], TextNode(" text", TextType.NORMAL))

    def test_front_italic_split(self):
        text = TextNode("*this* text has italic text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "*", TextType.ITALIC)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("this", TextType.ITALIC))
        self.assertEqual(result[1], TextNode(
            " text has italic text", TextType.NORMAL))

    def test_multiple_italic_split(self):
        text = TextNode("*this* text has *italic* text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "*", TextType.ITALIC)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], TextNode("this", TextType.ITALIC))
        self.assertEqual(result[1], TextNode(" text has ", TextType.NORMAL))
        self.assertEqual(result[2], TextNode("italic", TextType.ITALIC))
        self.assertEqual(result[3], TextNode(" text", TextType.NORMAL))

    def test_bold_split(self):
        text = TextNode("this text has **bold** text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" text", TextType.NORMAL))

    def test_code_split(self):
        text = TextNode("this text has `code` text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))
        self.assertEqual(result[2], TextNode(" text", TextType.NORMAL))

    def test_different_split(self):
        text = TextNode("*this* text has `code` text", TextType.NORMAL)
        result = split_nodes_delimiter([text], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "*this* text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))
        self.assertEqual(result[2], TextNode(" text", TextType.NORMAL))


class TestSplitNodesImages(unittest.TestCase):
    def test_no_split(self):
        text = TextNode("this text has no images", TextType.NORMAL)
        result = split_nodes_image([text])
        self.assertEqual(result[0], text)

    def test_one_image(self):
        text = TextNode(
            "this text has ![one image](image.url)", TextType.NORMAL)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one image", TextType.IMAGE, "image.url"))

    def test_middle_image(self):
        text = TextNode(
            "this text has ![one image](image.url) in the middle", TextType.NORMAL)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one image", TextType.IMAGE, "image.url"))
        self.assertEqual(result[2], TextNode(
            " in the middle", TextType.NORMAL))

    def test_multiple_images(self):
        text = TextNode(
            "this text has ![one image](image.url) in front of ![another image](another.image.url)", TextType.NORMAL)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one image", TextType.IMAGE, "image.url"))
        self.assertEqual(result[2], TextNode(
            " in front of ", TextType.NORMAL))
        self.assertEqual(result[3], TextNode(
            "another image", TextType.IMAGE, "another.image.url"))


class TestSplitNodesLink(unittest.TestCase):
    def test_no_split(self):
        text = TextNode("this text has no links", TextType.NORMAL)
        result = split_nodes_link([text])
        self.assertEqual(result[0], text)

    def test_one_link(self):
        text = TextNode(
            "this text has [one link](link.url)", TextType.NORMAL)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one link", TextType.LINK, "link.url"))

    def test_middle_link(self):
        text = TextNode(
            "this text has [one link](link.url) in the middle", TextType.NORMAL)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one link", TextType.LINK, "link.url"))
        self.assertEqual(result[2], TextNode(
            " in the middle", TextType.NORMAL))

    def test_multiple_link(self):
        text = TextNode(
            "this text has [one link](link.url) in front of [another link](another.link.url)", TextType.NORMAL)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], TextNode(
            "this text has ", TextType.NORMAL))
        self.assertEqual(result[1], TextNode(
            "one link", TextType.LINK, "link.url"))
        self.assertEqual(result[2], TextNode(
            " in front of ", TextType.NORMAL))
        self.assertEqual(result[3], TextNode(
            "another link", TextType.LINK, "another.link.url"))
