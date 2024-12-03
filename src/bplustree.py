import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from node import Node

class BPlusTree(object):
    """B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.

    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order=8):
        self.root = Node(order)

    def _find_position(self, node, key):
        """Finds the appropriate child node and index for the given key."""
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge_nodes(self, parent, child, index):
        """Merges a child node into the parent node by extracting a pivot key."""
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys.append(pivot)
                parent.values.extend(child.values)
                break

    def insert_key_value(self, key, value):
        """Inserts a key-value pair into the tree. Splits leaf nodes if full."""
        parent = None
        child = self.root

        # Traverse the tree until a leaf node is reached.
        while not child.leaf:
            parent = child
            child, index = self._find_position(child, key)

        child.insert_key_value(key, value)

        # Split the leaf node if it becomes full.
        if child.is_node_full():
            child.split_node()

            # If there is a parent and it is not full, merge the new nodes.
            if parent and not parent.is_node_full():
                self._merge_nodes(parent, child, index)

    def retrieve_value(self, key):
        """Retrieves the value for a given key, or None if the key does not exist."""
        child = self.root

        while not child.leaf:
            child, index = self._find_position(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def display_tree(self):
        """Displays the keys in the tree at each level."""
        self.root.display_keys()
