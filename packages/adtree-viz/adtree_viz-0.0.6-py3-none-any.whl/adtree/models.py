from __future__ import annotations

import hashlib
from typing import List


class Node(object):
    def __init__(self, label: str = "", child_nodes: List[Node] = None):
        self.label = label
        self.id = Node._hash(label)
        if child_nodes is None:
            self.child_nodes = []
        else:
            self.child_nodes = child_nodes

    def get_id(self) -> str:
        return self.id

    def get_label(self) -> str:
        return self.label

    def get_child_nodes(self) -> List[Node]:
        return self.child_nodes

    @staticmethod
    def _hash(label: str) -> str:
        return hashlib.md5(label.encode()).hexdigest()

    def __repr__(self):
        return f"{self.__class__.__name__}:{self.label}"


class Attack(Node):
    def __init__(self, label: str = "", child_nodes: List[Node] = None):
        super().__init__(label=label, child_nodes=child_nodes)


class Defence(Node):
    def __init__(self, label: str = "", child_nodes: List[Node] = None):
        super().__init__(label=label, child_nodes=child_nodes)


class AndGate(Node):
    def __init__(self, child_nodes: List[Node] = None):
        super().__init__(label="AND", child_nodes=child_nodes)
