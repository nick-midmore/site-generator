from extract import *
from splitdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

def split_nodes_image(old_nodes):
    result_nodes = []
    for n in old_nodes:
        original_text = n.text
        images = extract_images(original_text)
        if len(images) < 1 or n.text_type != TextType.TEXT:
            result_nodes.append(n)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                result_nodes.append(TextNode(sections[0], TextType.TEXT))
            result_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            result_nodes.append(TextNode(original_text, TextType.TEXT))
    return result_nodes


def split_nodes_link(old_nodes):    
    result_nodes = []
    for n in old_nodes:
        original_text = n.text
        links = extract_links(original_text)
        if len(links) < 1 or n.text_type != TextType.TEXT:
            result_nodes.append(n)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0]:
                result_nodes.append(TextNode(sections[0], TextType.TEXT))
            result_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text:
            result_nodes.append(TextNode(original_text, TextType.TEXT))
    return result_nodes

def text_to_textnodes(text):
    result_nodes = [TextNode(text, TextType.TEXT)]
    result_nodes = split_nodes_delimiter(result_nodes, "**", TextType.BOLD)
    result_nodes = split_nodes_delimiter(result_nodes, "_", TextType.ITALIC)
    result_nodes = split_nodes_delimiter(result_nodes, "`", TextType.CODE)
    result_nodes = split_nodes_image(result_nodes)
    result_nodes = split_nodes_link(result_nodes)
    return result_nodes
