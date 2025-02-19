from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes should always have a value")

        if self.tag is None:
            return self.value
        else:
            start_tag = f"<{self.tag}{self.props_to_html()}>"
            end_tag = f"</{self.tag}>"
            return f"{start_tag}{self.value}{end_tag}"
