from __future__ import annotations

import copy

from typing import TYPE_CHECKING, List, Optional, Type

from vypr.engine.value import VpValue
from vypr.engine.validator import VpValidator, VpNullValidator

if TYPE_CHECKING:
    from vypr.engine.graph import VpGraph


class VpNodePlugin:

    __slots__ = [
        "_node",
        "_node_cls",
        "_attr",
        "_attr_name",
    ]

    _node: VpNode
    _node_cls: Type[VpNode]
    _attr: str
    _attr_name: str

    def __get__(self, node, _):
        return node.__dict__[self._attr]

    def __set__(self, node, value):
        raise AttributeError(f"'{type(node).__name__}.{self._attr}' is read only")

    def __set_name__(self, node_cls: Type[VpNode], name: str):
        self._attr = name
        self._attr_name = f"{node_cls.__name__}.{name}"
        self._node_cls = node_cls

    def register(self, node):
        self._node = node

    @property
    def attr(self):
        return self._attr

    @property
    def attr_name(self):
        return self._attr_name

    @property
    def node(self):
        return self._node

    @property
    def node_type(self):
        return self._node_cls


class VpSocket(VpNodePlugin):
    def __init__(
        self,
        value: VpValue,
        validator: VpValidator = VpNullValidator(),
        label: str = "",
        help: str = "",
    ):
        self._value = value
        self._validator = validator
        self._label = label
        self._help = help

    def _default_label(self):
        label = self._attr or ""
        return " ".join([x.title() for x in label.split("_")])

    @property
    def label(self):
        return self._label or self._default_label()

    @property
    def path(self):
        if self.node:
            return f"{self.node.path}.{self.label}"
        return self.label

    def register(self, node):
        super().register(node)
        value = copy.copy(self._value)
        value.socket = self
        node.__dict__[self._attr] = value


class VpInput(VpSocket):
    def __init__(
        self,
        value: VpValue,
        validator: VpValidator = VpNullValidator(),
        label: str = "",
        help: str = "",
        connectable_types: Optional[List[Type[VpValue]]] = None,
    ):
        super().__init__(value=value, validator=validator, label=label, help=help)
        self._connectable_types = connectable_types

    def register(self, node):
        super().register(node)
        type(node)._inputs.append(self)


class VpOutput(VpSocket):
    def __init__(
        self,
        value: VpValue,
        validator: VpValidator = VpNullValidator(),
        label: str = "",
        help: str = "",
    ):
        super().__init__(value=value, validator=validator, label=label, help=help)

    def register(self, node):
        super().register(node)
        type(node)._outputs.append(self)


class VpEdit(VpNodePlugin):
    def __init__(self, widget, sockets, **kwargs):
        self._sockets = sockets
        self._widget = widget

    def register(self, node):
        super().register(node)
        widget = self._widget(self._sockets)
        node.__dict__[self._attr] = widget


class VpNode:

    __slots__ = ["_label", "_graph"]

    _inputs: List[VpSocket] = []
    _outputs: List[VpSocket] = []

    def __init__(self, label: str):
        self._label = label
        self._graph: Optional[VpGraph] = None

        # Install node plugin components.
        for value in vars(self.__class__).values():
            if isinstance(value, VpNodePlugin):
                value.register(self)

    @property
    def label(self):
        return self._label

    @property
    def graph(self):
        return self._graph

    @property
    def path(self):
        if self.graph:
            return f"{self.graph.path}/{self.label}"
        return f"/{self.label}"
