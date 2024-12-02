class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        # Initialize a B+ tree node
        # is_leaf indicates whether the node is a leaf node
        self.is_leaf = is_leaf
        self.keys = []  # List of keys in the node
        self.children = []  # List of child nodes (for internal nodes)
        self.values = [] if is_leaf else None  # List of values (only for leaf nodes)

    def __repr__(self):
        # String representation of the node for debugging
        return f"BPlusTreeNode(keys={self.keys}, is_leaf={self.is_leaf})"

class BPlusTree:
    def __init__(self, order=4):
        # Initialize a B+ tree
        # order is the maximum number of children a node can have
        self.order = order
        self.root = BPlusTreeNode(is_leaf=True)  # Start with an empty leaf node as the root

    def insert(self, key, value):
        # Insert a key-value pair into the B+ tree
        root = self.root
        # If the root is full, split it and create a new root
        if len(root.keys) == self.order - 1:
            new_root = BPlusTreeNode()  # Create a new root node
            new_root.children.append(self.root)  # Add current root as child of new root
            self._split_child(new_root, 0)  # Split the child
            self.root = new_root  # Update the root
        self._insert_non_full(self.root, key, value)  # Insert the key-value pair

    def _insert_non_full(self, node, key, value):
        # Helper function to insert a key-value pair into a non-full node
        if node.is_leaf:
            # If the node is a leaf, find the correct position and insert the key and value
            idx = self._find_index(node.keys, key)
            node.keys.insert(idx, key)
            node.values.insert(idx, value)
        else:
            # If the node is not a leaf, find the correct child to recurse into
            idx = self._find_index(node.keys, key)
            child = node.children[idx]
            # If the child is full, split it
            if len(child.keys) == self.order - 1:
                self._split_child(node, idx)
                # Determine which of the two children to recurse into
                if key > node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.children[idx], key, value)

    def _split_child(self, parent, index):
        # Helper function to split a child node that is full
        node_to_split = parent.children[index]
        new_node = BPlusTreeNode(is_leaf=node_to_split.is_leaf)  # Create a new node
        mid = len(node_to_split.keys) // 2  # Find the middle index

        # Insert the middle key into the parent
        parent.keys.insert(index, node_to_split.keys[mid])
        parent.children.insert(index + 1, new_node)  # Add the new node as a child

        # Split the keys between the original node and the new node
        new_node.keys = node_to_split.keys[mid + 1:]
        node_to_split.keys = node_to_split.keys[:mid]

        if node_to_split.is_leaf:
            # If the node to split is a leaf, split the values as well
            new_node.values = node_to_split.values[mid + 1:]
            node_to_split.values = node_to_split.values[:mid]
            # Maintain the linked list structure of leaf nodes
            new_node.next = node_to_split.next
            node_to_split.next = new_node
        else:
            # If the node is not a leaf, split the children
            new_node.children = node_to_split.children[mid + 1:]
            node_to_split.children = node_to_split.children[:mid + 1]

    def _find_index(self, keys, key):
        # Find the index at which to insert a key in a sorted list of keys
        idx = 0
        while idx < len(keys) and key > keys[idx]:
            idx += 1
        return idx

    def search(self, key):
        # Search for a key in the B+ tree and return its value if found
        leaf_node = self._find_leaf_node(key)  # Find the leaf node where the key might be
        for i, k in enumerate(leaf_node.keys):
            if k == key:
                return leaf_node.values[i]  # Return the value if the key is found
        return None  # Return None if the key is not found

    def _find_leaf_node(self, key):
        # Find the leaf node that should contain the given key
        current_node = self.root
        while not current_node.is_leaf:
            idx = self._find_index(current_node.keys, key)
            current_node = current_node.children[idx]  # Traverse down to the correct child
        return current_node
