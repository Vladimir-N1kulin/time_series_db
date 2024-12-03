class Node(object):
    """Base node object.

    Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.

    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium to traverse the tree."""
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def insert_key_value(self, key, value):
        """Inserts a key-value pair into the node."""
        # If the node is empty, simply insert the key-value pair.
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            # If new key matches an existing key, add to the list of values.
            if key == item:
                self.values[i].append(value)
                break

            # If new key is smaller than an existing key, insert the new key to the left of it.
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # If new key is larger than all existing keys, insert it at the end.
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])

    def split_node(self):
        """Splits the node into two child nodes."""
        left_child = Node(self.order)
        right_child = Node(self.order)
        mid_index = self.order // 2

        left_child.keys = self.keys[:mid_index]
        left_child.values = self.values[:mid_index]

        right_child.keys = self.keys[mid_index:]
        right_child.values = self.values[mid_index:]

        # Set the parent key to the left-most key of the right child node.
        self.keys = [right_child.keys[0]]
        self.values = [left_child, right_child]
        self.leaf = False

    def is_node_full(self):
        """Checks if the node has reached its maximum capacity."""
        return len(self.keys) == self.order

    def display_keys(self, depth=0):
        """Displays the keys in the node at each level."""
        print(depth, str(self.keys))

        # Recursively display the keys of child nodes (if any exist).
        if not self.leaf:
            for child in self.values:
                child.display_keys(depth + 1)
