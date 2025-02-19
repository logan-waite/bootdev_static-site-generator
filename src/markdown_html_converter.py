import utils
from parentnode import ParentNode


def markdown_to_html_node(markdown):
    # Split markdown into blocks
    blocks = utils.markdown_to_blocks(markdown)

    all_nodes = []
    # For each block:
    for block in blocks:
        #   determine block type
        block_type = utils.block_to_block_type(block)
        #   create children html nodes (TextNode -> HTMLNode)
        lines = utils.get_block_lines(block, block_type)
        children_nodes = []
        for line in lines:
            text_nodes = utils.text_to_textnodes(line)
            child_nodes = [utils.text_node_to_html_node(
                text_node) for text_node in text_nodes]
            if block_type == 'unordered_list' or block_type == 'ordered_list':
                child_nodes = [ParentNode('li', child_nodes)]
            children_nodes.extend(child_nodes)

        #   create an html node based on the block type
        tag = utils.get_block_type_tag(block_type)
        node = ParentNode(tag, children_nodes)

        all_nodes.append(node)

    # Put all these blocks under a single parent div
    return ParentNode('div', all_nodes)
