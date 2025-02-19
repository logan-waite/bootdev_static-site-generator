class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        props_string = ""
        for (key, value) in self.props.items():
            props_string += f" {key}=\"{value}\""

        return props_string

    def __repr__(self):
        return f"""`TAG: {self.tag},\n
            VALUE: {self.value},\n
            CHILDREN: {self.children},\n
            PROPS: {self.props}`"""
