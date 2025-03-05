from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            first_split = n.text.split(delimiter, 1)
            if len(first_split) > 1:
                initial_text = first_split[0]
                remainder_text = first_split[1]
                second_split = remainder_text.split(delimiter, 1)
                if len(second_split) > 1:
                    enclosed_text = second_split[0]
                    end_text = second_split[1]
                    new_nodes.extend(
                        [ 
                            TextNode(initial_text, TextType.TEXT),
                            TextNode(enclosed_text, text_type),
                            TextNode(end_text, TextType.TEXT)
                        ])
                else:
                    raise Exception("No closing delimiter found - invalid markdown")
        else:
            new_nodes.append(n)