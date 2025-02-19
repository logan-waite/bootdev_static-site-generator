import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_inits_with_all_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_single_prop_to_html(self):
        node = HTMLNode(props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"www.google.com\"")

    def test_multiple_props_to_html(self):
        props = {"href": "www.google.com", "target": "_blank"}
        expected = " href=\"www.google.com\" target=\"_blank\""
        node = HTMLNode(props=props)
        actual = node.props_to_html()
        self.assertEqual(expected, actual)
