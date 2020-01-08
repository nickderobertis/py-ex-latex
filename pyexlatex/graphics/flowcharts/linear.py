from typing import Sequence, Union, Optional, List, cast
from copy import deepcopy
from pyexlatex.models.item import ItemBase
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.graphics.tikz.node.node import Node
from pyexlatex.graphics import Arrow
from pyexlatex.graphics.tikz.node.position.directions import Right, Below


class LinearFlowchart(ContainerItem, ItemBase):
    """
    Creates a linear flow chart (nodes with arrows in between), going horizontally or vertically from one item
    to the next.
    """

    def __init__(self, steps: Sequence[Union[Node, str]], horizontal: bool = True,
                 node_options: Optional[List[str]] = None):
        self.steps = steps
        self.horizontal = horizontal
        self.node_options = node_options
        self.add_data_from_content(steps)
        self.nodes = self._get_nodes()
        self.contents = self._get_contents()

    def __str__(self) -> str:
        from pyexlatex.logic.builder import _build
        if isinstance(self.contents, (list, tuple)):
            return _build(self.contents)
        else:
            return str(self.contents)

    def _get_contents(self) -> List[Union[Node, Arrow]]:
        nodes = self.nodes
        contents = deepcopy(nodes)
        for i, node in enumerate(nodes):
            if i == 0:
                continue
            contents.append(Arrow(nodes[i - 1], nodes[i]))
        self.add_data_from_content(contents)
        return contents

    def _get_nodes(self) -> List[Node]:
        out_nodes = []
        for i, item in enumerate(self.steps):
            if hasattr(item, 'is_Node') and item.is_Node:  # type: ignore
                node_item: Node = cast(Node, item)
                if i == 0:
                    out_nodes.append(node_item)
                    continue
                # If beyond the first element, need to create a new node with the same info, but with
                # position relative to the last element
                new_node = Node(
                    contents=node_item.content,
                    location=self.direction(of=out_nodes[i - 1]),
                    label=node_item.label,
                    options=node_item.options,
                    overlay=node_item.overlay
                )
                new_node.add_data_from_content(node_item)
                out_nodes.append(
                    new_node
                )
            else:
                # Treat as str passed, need to create node with str and node options
                out_nodes.append(
                    Node(
                        contents=item,
                        location=self.direction(of=out_nodes[i - 1]) if i > 0 else None,
                        options=self.node_options
                    )
                )
        return out_nodes

    @property
    def direction(self) -> type:
        if self.horizontal:
            return Right
        else:
            return Below
