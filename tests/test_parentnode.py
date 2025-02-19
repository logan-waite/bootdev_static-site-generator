import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_tag_required_in_init(self):
        with self.assertRaises(TypeError):
            ParentNode(children=[])

    def test_children_required_in_init(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="a")

    def test_tag_required(self):
        with self.assertRaises(ValueError) as err:
            node = ParentNode(tag=None, children=[])
            node.to_html()
            self.assertEqual(err.exception, "Tag is required")

    def test_children_required(self):
        with self.assertRaises(ValueError) as err:
            node = ParentNode(tag="a", children=None)
            node.to_html()
            self.assertEqual(err.exception, "Children is required")
            node2 = ParentNode(tag="div", children=[])
            node2.to_html()
            self.assertEqual(err.exception, "Children is required")

    def test_all_args(self):
        node = ParentNode("a", [], props={'href': 'google.com'})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'href': 'google.com'})

    def test_to_html_with_one_child(self):
        node = ParentNode("div", [LeafNode('p', 'some text')])
        self.assertEqual(node.to_html(), "<div><p>some text</p></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "div",
            [LeafNode('p', 'some text'), LeafNode('span', 'more text')]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>some text</p><span>more text</span></div>"
        )

    def test_to_html_nested(self):
        node = ParentNode(
            "div", [ParentNode('p', [LeafNode('span', 'some text')])])
        self.assertEqual(
            node.to_html(), "<div><p><span>some text</span></p></div>")

    def test_to_html_multiple_children_nested(self):
        node = ParentNode("div", [ParentNode(
            'p', [LeafNode('span', 'some text')]), LeafNode('b', 'bold')])
        self.assertEqual(
            node.to_html(),
            "<div><p><span>some text</span></p><b>bold</b></div>"
        )

    def test_to_html_nested_props(self):
        node = ParentNode(
            "div",
            [ParentNode(
                'p',
                [LeafNode('span', 'some text')],
                props={'style': 'color: red'})]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p style=\"color: red\"><span>some text</span></p></div>"
        )
