import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            split = n.text.split(delimiter, 2)
            if len(split) == 3:
                start_text = split[0]
                middle_text = split[1]
                end_text = split[2]
                if not start_text:
                    new_nodes.extend(
                        [
                            TextNode(middle_text, text_type),
                            TextNode(end_text, TextType.TEXT)
                        ]
                    )
                elif not end_text:
                    new_nodes.extend(
                        [
                            TextNode(start_text, TextType.TEXT),
                            TextNode(middle_text, text_type)
                        ]
                    )
                else:
                    result_nodes = [
                            TextNode(start_text, TextType.TEXT),
                            TextNode(middle_text, text_type),
                        ]
                    result_nodes.extend(split_nodes_delimiter([TextNode(end_text, TextType.TEXT)], delimiter, text_type))
                    new_nodes.extend(result_nodes)
            elif len(split) == 2:
                raise Exception("No closing delimiter found - invalid markdown")
            else:
                new_nodes.append(n)
        else:
            new_nodes.append(n)
    return new_nodes


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


def extract_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
