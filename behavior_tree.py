import logging


class Node:
    def __init__(self, name: str, action):
        self.name = name
        self.action = action

    def run(self) -> bool:
        logging.debug(f"Running Node {self.name}")
        return self.action()


class SequenceNode(Node):
    def __init__(self, name: str, nodes: [Node]):
        super().__init__(name, None)
        self.nodes = nodes

    def run(self) -> bool:
        logging.debug(f"Running SequenceNode {self.name}")
        any_succeeded = False
        for node in self.nodes:
            if node.run():
                any_succeeded = True
            else:
                return any_succeeded
        return any_succeeded


class SelectorNode(SequenceNode):
    def __init__(self, name: str, nodes: [Node]):
        super().__init__(name, nodes)

    def run(self) -> bool:
        logging.debug(f"Running SelectorNode {self.name}")
        for node in self.nodes:
            if node.run():
                return True
        return False


class TrueDecorator(Node):
    def __init__(self, name: str, node: Node):
        super().__init__(name, None)
        self.node = node

    def run(self) -> bool:
        logging.debug(f"Running True Decorator {self.name}")
        self.node.run()
        return True


class BehaviorTree:
    def __init__(self, root_node: Node):
        self.root_node = root_node

    def run(self):
        self.root_node.run()
