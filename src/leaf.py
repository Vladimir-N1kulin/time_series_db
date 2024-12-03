import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from node import Node
class Leaf(Node):
    def __init__(self, parent=None, prev_node=None, next_node=None):
        """
        Create a new leaf in the leaf link
        :type prev_node: Leaf
        :type next_node: Leaf
        """
        super(Leaf, self).__init__(parent)
        self.next: Leaf = next_node
        if next_node is not None:
            next_node.prev = self
        self.prev: Leaf = prev_node
        if prev_node is not None:
            prev_node.next = self

        self.splits = 0
        self.fusions = 0

    def __getitem__(self, item):
        return self.values[self.keys.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.values[i:i] = [value]
        else:
            self.values[i - 1] = value

    def split(self):
        """Splits the leaf into two and links them in the leaf list."""
        self.splits += 1

        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        self.keys: list = self.keys[mid:]
        self.values: list = self.values[mid:]

        # When the leaf node is split, set the parent key to the left-most key of the right child node.
        return self.keys[0], [left, self]

    def __delitem__(self, key):
        i = self.keys.index(key)
        del self.keys[i]
        del self.values[i]

    def fusion(self):
        """Merges this leaf with a sibling leaf."""
        self.fusions += 1

        index = self.parent.index(self.keys[0])

        # Merge this node with the next node
        if index < len(self.parent.keys):
            next_node: Leaf = self.parent.values[index + 1]
            next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
            next_node.values[0:0] = self.values

            # Update the parent to remove the merged key
            del self.parent.keys[index]
            del self.parent.values[index]

        else:  # If this is the last node, merge with the previous node
            prev_node: Leaf = self.parent.values[index - 1]
            prev_node.keys += [self.parent.keys[index - 1]] + self.keys
            prev_node.values += self.values

            # Update the parent to remove the merged key
            del self.parent.keys[index - 1]
            del self.parent.values[index]

        # Update sibling links
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next



    def borrow_key(self, minimum: int):
        """Borrows a key from a sibling leaf to balance the tree."""
        index = self.parent.index(self.keys[0])

        # Borrow from the next sibling
        if index < len(self.parent.keys):
            next_node: Leaf = self.parent.values[index + 1]
            if len(next_node.keys) > minimum:
                self.keys += [self.parent.keys[index]]

                borrow_value = next_node.values.pop(0)
                self.values += [borrow_value]
                self.parent.keys[index] = next_node.keys.pop(0)
                return True

        # Borrow from the previous sibling
        elif index != 0:
            prev_node: Leaf = self.parent.values[index - 1]
            if len(prev_node.keys) > minimum:
                self.keys[0:0] = [self.parent.keys[index - 1]]

                borrow_value = prev_node.values.pop()
                self.values[0:0] = [borrow_value]
                self.parent.keys[index - 1] = prev_node.keys.pop()
                return True

        return False



