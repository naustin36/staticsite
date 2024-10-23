from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Extracts any valid markdown of the type specified from TextNodes with TEXT type, and returns a new list of TextNodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown: missing {delimiter}")
        strings = node.text.split(delimiter)
        for i in range(len(strings)):
            if strings[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(strings[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(strings[i], text_type))
        
    return new_nodes
            