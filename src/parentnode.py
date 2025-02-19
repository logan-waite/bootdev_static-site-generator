from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")
        if not self.children:
            raise ValueError("Children is required")

        result = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            result += node.to_html()

        result += f"</{self.tag}>"

        return result
