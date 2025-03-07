from extract import *
from textnode import TextNode, TextType


def split_nodes_image(old_nodes):
    result_nodes = []
    for n in old_nodes:
        images = extract_images(n.text)
        if len(images) < 1:
            result_nodes.append(n)
            continue
        for image in images:
            image_node_text = f"![{image[0]}]({image[1]})"
            sections = n.text.split(image_node_text, 1)
            new_nodes = []
            if not sections[0]:
                result_nodes.append(TextNode(images[0], TextType.IMAGE, images[1]))
                new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
                result_nodes.extend(new_nodes)
            elif not sections[1]:
                result_nodes.extend([TextNode(sections[0], TextType.TEXT), TextNode(images[0], TextType.IMAGE, images[1])])
            else:
                new_nodes.extend([TextNode(sections[0], TextType.TEXT), TextNode(images[0], TextType.IMAGE, images[1])])
                new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
                result_nodes.extend(new_nodes)




def split_nodes_link(old_nodes):    
    pass