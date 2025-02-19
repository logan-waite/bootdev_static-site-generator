import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_children(self):
        with self.assertRaises(TypeError):
            LeafNode(None, None, children=[])

    def test_requires_value(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

        with self.assertRaises(ValueError):
            node = LeafNode(None, None)
            node.to_html()
