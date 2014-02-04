class SetForestNode(object):
    """A node in a Disjoint Set Forest."""
    def __init__(self, item):
        self.data = item
        self.parent = item

class SetForest(object):
    """Implementation of a Disjoint Set Forest to use the Union-Find
    algorithms."""
    def __init__(self, items):
        self.nodes = {item: SetForestNode(item) for item in items}

    def find(self, item):
        node = self.nodes[item]
        if node.data is not node.parent:
            node.parent = self.nodes[self.find(node.parent)].data
        return node.parent

    def union(self, nodeA, nodeB):
        rootA = self.nodes[self.find(nodeA)]
        rootB = self.nodes[self.find(nodeB)]

        rootB.parent = rootA.data
