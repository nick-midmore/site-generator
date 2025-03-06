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