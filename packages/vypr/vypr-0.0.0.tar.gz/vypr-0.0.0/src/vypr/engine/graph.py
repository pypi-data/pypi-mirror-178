from typing import Iterable, Optional, Type

from vypr.engine.node import VpNode


class VpGraph:

    __slots__ = [
        "_graph",
        "_nodes",
        "_node_types",
        "_label",
    ]

    NODE_TYPES: Iterable[Type[VpNode]] = []

    def __init__(self, label: str, node_types: Optional[Iterable[Type[VpNode]]]):
        self._graph = None
        self._nodes = {}
        self._node_types = node_types or self.NODE_TYPES

        self._label = label

    def add_node(self, node_type, name):
        node = node_type(name)
        node._graph = self
        self._nodes[name] = node
        return node

    def get_node(self, name):
        return self._nodes[name]

    @property
    def graph(self):
        return self._graph

    @property
    def label(self):
        return self._label

    @property
    def path(self):
        if self.graph:
            return f"{self.graph.path}/{self.label}"
        return f"/{self.label}"
