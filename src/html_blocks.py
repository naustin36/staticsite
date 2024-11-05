from htmlnode import *
from inline_markdown import *
from textnode import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "paragraph":
            html_blocks.append(paragraph_block_to_html_nodes(block))
        elif block_type == "heading":
            html_blocks.append(heading_block_to_html_nodes(block))
        elif block_type == "code":
            html_blocks.append(code_block_to_html_nodes(block))
        elif block_type == "quote":
            html_blocks.append(quote_block_to_html_nodes(block))
        elif block_type == "unordered_list":
            html_blocks.append(list_block_to_html_nodes(block, block_type))
        elif block_type == "ordered_list":
            html_blocks.append(list_block_to_html_nodes(block, block_type))

    return ParentNode("div", html_blocks)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
            
def paragraph_block_to_html_nodes(block):
    child_nodes = text_to_children(block)
    return ParentNode("p", child_nodes)

def heading_block_to_html_nodes(block):
    heading_markdown = block.split()[0]
    heading_count = heading_markdown.count("#")
    tag = f"h{heading_count}"
    child_nodes = text_to_children(block.lstrip("# "))
    return ParentNode(tag, child_nodes)

def code_block_to_html_nodes(block):
    child_nodes = text_to_children(block)
    return ParentNode("pre", child_nodes)

def quote_block_to_html_nodes(block):
    lines = block.split("\n")
    filtered_lines = []
    for line in lines:
        line = line.lstrip(">")
        line = line.strip()
        filtered_lines.append(line)
    filtered_block = "\n".join(filtered_lines)
    child_nodes = text_to_children(filtered_block)
    return ParentNode("blockquote", child_nodes)

def list_block_to_html_nodes(block, block_type):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        line = " ".join(line.split()[1:])
        text_nodes = text_to_textnodes(line)
        child_nodes = []
        for node in text_nodes:
            child_nodes.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode("li", child_nodes))
    if block_type == "unordered_list":
        return ParentNode("ul", html_nodes)
    if block_type == "ordered_list":
        return ParentNode("ol", html_nodes)
    
    
    






        
