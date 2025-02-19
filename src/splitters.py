import re
from textnode import TextNode, TextType
from consts import image_regex, link_regex


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image_or_text(old_nodes, regex, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(regex, old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 3 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            if i % 3 == 1:
                split_nodes.append(
                    TextNode(sections[i], text_type, sections[i+1]))
            if i % 3 == 2:
                # Used the link in previous iteration
                continue
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_image_or_text(old_nodes, image_regex, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes_image_or_text(old_nodes, link_regex, TextType.LINK)
