import re
from textnode import TextNode, TextType
from leafnode import LeafNode
from splitters import split_nodes_delimiter, split_nodes_link, split_nodes_image
from consts import image_regex, link_regex


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                'img',
                "",
                {'src': text_node.url, 'alt': text_node.text}
            )
        case _:
            raise Exception("unknown text type")


def extract_markdown_images(text):
    matches = re.findall(image_regex, text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(link_regex, text)

    return matches


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.NORMAL)
    nodes = [initial_node]
    for (delimiter, text_type) in [('**', TextType.BOLD), ('_', TextType.ITALIC),  ('`', TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    nodes_with_images = split_nodes_image(nodes)
    nodes_with_links = split_nodes_link(nodes_with_images)
    return nodes_with_links


def markdown_to_blocks(markdown):
    return list(map(lambda r: r.strip(), markdown.split("\n\n")))


paragraph = "paragraph"
heading = "heading"
code = "code"
quote = "blockquote"
unordered_list = "unordered_list"
ordered_list = "ordered_list"


def block_to_block_type(markdown):
    header_tags = ['# ', '## ', '### ', '#### ', '##### ', '###### ']
    lines = markdown.split('\n')
    if any([markdown.startswith(tag) for tag in header_tags]):
        match = re.findall(r"#+", markdown)[0]
        return heading + str(len(match))
    elif markdown.startswith("```\n") and markdown.endswith("\n```"):
        return code
    elif all([line.startswith(">") for line in lines]):
        return quote
    elif all([line.startswith("* ") for line in lines]):
        return unordered_list
    elif all([line.startswith("- ") for line in lines]):
        return unordered_list
    elif all([line.startswith(f"{i+1}. ") for i, line in enumerate(lines)]):
        return ordered_list
    else:
        return paragraph


def get_block_lines(block, block_type=None):
    lines = list(map(lambda line: line.strip(), block.split('\n')))
    if block_type and heading in block_type:
        return [line.replace('#', '').strip() for line in lines]
    elif block_type == code:
        return lines[1:-1]
    elif block_type == quote:
        return [line.lstrip("> ") for line in lines]
    elif block_type == unordered_list:
        return [line[2:] for line in lines]
    elif block_type == ordered_list:
        return [line[3:] for line in lines]
    else:
        return lines


def get_block_type_tag(block_type):
    if block_type == paragraph:
        return 'p'
    elif heading in block_type:
        return 'h' + block_type[-1]
    elif block_type == unordered_list:
        return "ul"
    elif block_type == ordered_list:
        return "ol"
    else:
        return block_type
