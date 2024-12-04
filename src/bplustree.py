
import random  # For generating random values in demo tests

# Global counters to track operations performed on the B+ Tree
splits = 0  # Number of node splits
parent_splits = 0  # Number of splits involving parent nodes
fusions = 0  # Number of node merges (fusions)
parent_fusions = 0  # Number of fusions involving parent nodes


class Node(object):
    """
    Base class for internal nodes in the B+ Tree.
    These nodes store keys and pointers to child nodes (values).
    Attributes:
        - parent: Reference to the parent node.
    """

    def __init__(self, parent=None):
        """
        Initialize a node.
        :param parent: Parent node, if any.
        """
        self.keys: list = []  # List of keys stored in the node
        self.values: list[Node] = []  # List of pointers to child nodes or data
        self.parent: Node = parent  # Reference to the parent node

    def index(self, key):
        """
        Find the position where a given key fits within the current node's keys.
        :param key: The key to find the position for.
        :return: Index position of the key.
        """
        for i, item in enumerate(self.keys):
            if key < item:  # If key is smaller than the current key, return index
                return i
        return len(self.keys)  # If key is larger than all, return the last position

    def __getitem__(self, item):
        """
        Retrieve the child node corresponding to a given key.
        :param item: The key for which to retrieve the child node.
        :return: The child node at the computed index.
        """
        return self.values[self.index(item)]

    def __setitem__(self, key, value):
        """
        Insert a key-value pair into the current node.
        :param key: The key to insert.
        :param value: The associated value (usually a pointer to a child node).
        """
        i = self.index(key)  # Find the correct position
        self.keys[i:i] = [key]  # Insert the key at the computed position
        self.values.pop(i)  # Remove the old value
        self.values[i:i] = value  # Insert the new value

    def split(self):
        """
        Split the current node when it exceeds the maximum capacity.
        Create a new left node and redistribute keys/values between the nodes.
        :return: The middle key and the two resulting nodes (left and self).
        """
        global splits, parent_splits
        splits += 1
        parent_splits += 1

        # Create a new node for the left half of the split
        left = Node(self.parent)

        mid = len(self.keys) // 2  # Find the middle index

        # Assign keys and values to the left node
        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]

        # Update parent references for the left node's children
        for child in left.values:
            child.parent = left

        # Update the current node to hold the right half of the split
        key = self.keys[mid]  # The middle key moves up to the parent
        self.keys = self.keys[mid + 1:]  # Retain only the right portion of keys
        self.values = self.values[mid + 1:]  # Retain only the right portion of values

        return key, [left, self]  # Return the key and two resulting nodes

    def __delitem__(self, key):
        """
        Remove a key and its associated value from the current node.
        :param key: The key to remove.
        """
        i = self.index(key)
        del self.values[i]  # Remove the value
        if i < len(self.keys):  # If the key is not at the end
            del self.keys[i]
        else:
            del self.keys[i - 1]  # If at the end, remove the previous key

    def fusion(self):
        """
        Merge the current node with its sibling when it falls below the minimum capacity.
        Updates the parent's keys and values accordingly.
        """
        global fusions, parent_fusions
        fusions += 1
        parent_fusions += 1

        # Get the index of the current node in the parent's values
        index = self.parent.index(self.keys[0])

        # If the current node is not the last child, merge with the next sibling
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            # Combine keys and values of both nodes
            next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
            for child in self.values:
                child.parent = next_node  # Update parent references
            next_node.values[0:0] = self.values
        else:
            # If the current node is the last child, merge with the previous sibling
            prev: Node = self.parent.values[-2]
            prev.keys += [self.parent.keys[-1]] + self.keys
            for child in self.values:
                child.parent = prev  # Update parent references
            prev.values += self.values

    def borrow_key(self, minimum: int):
        """
        Borrow a key from a sibling node to satisfy the minimum key requirement.
        :param minimum: The minimum number of keys a node should have.
        :return: True if a key was successfully borrowed, False otherwise.
        """
        index = self.parent.index(self.keys[0])  # Get the current node's index in the parent

        # Attempt to borrow a key from the next sibling
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            if len(next_node.keys) > minimum:
                # Borrow the smallest key from the next sibling
                self.keys += [self.parent.keys[index]]
                borrow_node = next_node.values.pop(0)  # Remove the corresponding value
                borrow_node.parent = self  # Update the parent reference
                self.values += [borrow_node]
                self.parent.keys[index] = next_node.keys.pop(0)  # Update the parent's key
                return True
        # Attempt to borrow a key from the previous sibling
        elif index != 0:
            prev: Node = self.parent.values[index - 1]
            if len(prev.keys) > minimum:
                # Borrow the largest key from the previous sibling
                self.keys[0:0] = [self.parent.keys[index - 1]]
                borrow_node = prev.values.pop()  # Remove the corresponding value
                borrow_node.parent = self  # Update the parent reference
                self.values[0:0] = [borrow_node]
                self.parent.keys[index - 1] = prev.keys.pop()  # Update the parent's key
                return True

        return False  # If borrowing is not possible, return False



class Leaf(Node):
    """
    Represents a leaf node in the B+ Tree.
    Leaf nodes store key-value pairs and are linked to other leaf nodes in a doubly linked list.
    """

    def __init__(self, parent=None, prev_node=None, next_node=None):
        """
        Initialize a leaf node.
        :param parent: Reference to the parent node.
        :param prev_node: Reference to the previous leaf node in the linked list.
        :param next_node: Reference to the next leaf node in the linked list.
        """
        super(Leaf, self).__init__(parent)  # Call the parent class (Node) initializer
        self.next: Leaf = next_node  # Pointer to the next leaf in the linked list
        if next_node is not None:
            next_node.prev = self  # Update the previous reference in the next node
        self.prev: Leaf = prev_node  # Pointer to the previous leaf in the linked list
        if prev_node is not None:
            prev_node.next = self  # Update the next reference in the previous node

    def __getitem__(self, item):
        """
        Retrieve the value(s) associated with a key.
        :param item: The key to search for.
        :return: The value(s) associated with the key.
        """
        return self.values[self.keys.index(item)]  # Locate the value using the key's index

    def __setitem__(self, key, value):
        """
        Insert or update a key-value pair in the leaf node.
        :param key: The key to insert or update.
        :param value: The value to associate with the key.
        """
        i = self.index(key)  # Determine the correct position for the key
        if key not in self.keys:
            self.keys.insert(i, key)  # Insert the key at the correct position
            self.values.insert(i, [value])  # Store the value in a list to handle duplicates
        else:
            self.values[i].append(value)  # Append the value to the existing list for duplicates

    def split(self):
        """
        Split the leaf node when it exceeds capacity.
        :return: The smallest key of the right node (current node) and the two resulting nodes.
        """
        global splits
        splits += 1  # Increment the global counter for splits

        # Create a new left leaf node for the split
        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2  # Find the middle index for splitting

        # Assign keys and values to the left node
        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        # Retain the remaining keys and values in the current node (right node)
        self.keys: list = self.keys[mid:]
        self.values: list = self.values[mid:]

        # Return the smallest key of the right node and the two resulting nodes
        return self.keys[0], [left, self]

    def __delitem__(self, key):
        """
        Remove a key and its associated value from the leaf node.
        :param key: The key to remove.
        """
        i = self.keys.index(key)  # Locate the index of the key
        del self.keys[i]  # Remove the key
        del self.values[i]  # Remove the associated value

    def fusion(self):
        """
        Merge the current leaf node with its neighbor when it falls below the minimum capacity.
        Updates the linked list and parent pointers accordingly.
        """
        global fusions
        fusions += 1  # Increment the global counter for fusions

        # If the next leaf is available and has the same parent, merge with it
        if self.next is not None and self.next.parent == self.parent:
            self.next.keys[0:0] = self.keys  # Prepend the keys from the current node
            self.next.values[0:0] = self.values  # Prepend the values from the current node
        else:
            # Otherwise, merge with the previous leaf
            self.prev.keys += self.keys  # Append the keys to the previous node
            self.prev.values += self.values  # Append the values to the previous node

        # Update the linked list pointers
        if self.next is not None:
            self.next.prev = self.prev  # Update the previous pointer of the next node
        if self.prev is not None:
            self.prev.next = self.next  # Update the next pointer of the previous node

    def borrow_key(self, minimum: int):
        """
        Borrow a key from a sibling leaf to maintain the minimum key count.
        :param minimum: The minimum number of keys required in a leaf node.
        :return: True if a key was successfully borrowed, False otherwise.
        """
        index = self.parent.index(self.keys[0])  # Find the index of this node in the parent

        # Attempt to borrow a key from the next sibling
        if index < len(self.parent.keys) and len(self.next.keys) > minimum:
            self.keys.append(self.next.keys.pop(0))  # Borrow the smallest key from the next sibling
            self.values.append(self.next.values.pop(0))  # Borrow the corresponding value
            self.parent.keys[index] = self.next.keys[0]  # Update the parent's key
            return True

        # Attempt to borrow a key from the previous sibling
        elif index != 0 and len(self.prev.keys) > minimum:
            self.keys.insert(0, self.prev.keys.pop())  # Borrow the largest key from the previous sibling
            self.values.insert(0, self.prev.values.pop())  # Borrow the corresponding value
            self.parent.keys[index - 1] = self.keys[0]  # Update the parent's key
            return True

        return False  # Return False if no borrowing is possible

class BPlusTree(object):
    """
    Represents a B+ tree, consisting of nodes (internal and leaf).
    Automatically handles node splits when a node exceeds its maximum capacity.
    Attributes:
        maximum (int): Maximum number of keys each node can hold.
    """

    def __init__(self, maximum=4):
        """
        Initialize a B+ Tree.
        :param maximum: Maximum number of keys per node. Default is 4.
        """
        self.root = Leaf()  # Start with a single root leaf node
        self.maximum: int = maximum if maximum > 2 else 2  # Minimum capacity is 2
        self.minimum: int = self.maximum // 2  # Minimum number of keys per node
        self.depth = 0  # Tree depth starts at 0

    def find(self, key) -> Leaf:
        """
        Locate the leaf node that should contain the given key.
        :param key: The key to find.
        :return: The leaf node where the key resides or should reside.
        """
        node = self.root
        # Traverse the tree from the root until reaching a leaf node
        while type(node) is not Leaf:
            node = node[key]  # Move to the child node based on the key
        return node

    def __getitem__(self, item):
        """
        Retrieve the value(s) associated with a given key.
        :param item: The key to search for.
        :return: The value(s) associated with the key.
        """
        return self.find(item)[item]  # Locate the key in the corresponding leaf

    def query(self, key):
        """
        Search for a key and return its value(s), or None if the key does not exist.
        :param key: The key to search for.
        :return: The value(s) associated with the key, or None.
        """
        leaf = self.find(key)  # Find the leaf containing the key
        return leaf[key] if key in leaf.keys else None  # Return the value(s) or None

    def change(self, key, value):
        """
        Update the value associated with a key.
        :param key: The key to update.
        :param value: The new value to associate with the key.
        :return: A tuple (bool, Leaf) indicating success and the leaf node.
        """
        leaf = self.find(key)  # Locate the leaf containing the key
        if key not in leaf.keys:
            return False, leaf  # Key does not exist
        else:
            leaf[key] = value  # Update the key-value pair
            return True, leaf

    def __setitem__(self, key, value, leaf=None):
        """
        Insert or update a key-value pair in the tree.
        Split the leaf node if it exceeds maximum capacity.
        :param key: The key to insert or update.
        :param value: The value to associate with the key.
        :param leaf: The leaf node to start insertion. If None, the correct leaf is located.
        """
        if leaf is None:
            leaf = self.find(key)  # Find the appropriate leaf for the key
        leaf[key] = value  # Insert or update the key-value pair
        if len(leaf.keys) > self.maximum:
            self.insert_index(*leaf.split())  # Split the node if it exceeds capacity

    def insert(self, key, value):
        """
        Insert a new key-value pair into the tree.
        :param key: The key to insert.
        :param value: The value to associate with the key.
        :return: A tuple (bool, Leaf) indicating success and the leaf node.
        """
        leaf = self.find(key)  # Locate the leaf for the key
        if key in leaf.keys:
            return False, leaf  # Key already exists
        else:
            self.__setitem__(key, value, leaf)  # Insert the key-value pair
            return True, leaf

    def insert_index(self, key, values: list[Node]):
        """
        Insert a key and associated child nodes into the parent node.
        :param key: The key to insert into the parent.
        :param values: The child nodes resulting from a split.
        """
        parent = values[1].parent  # Parent of the right node after the split
        if parent is None:
            # Create a new root if no parent exists
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1  # Increase tree depth
            self.root.keys = [key]  # Set the new root's key
            self.root.values = values  # Set the new root's children
            return

        parent[key] = values  # Insert the key and children into the parent
        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())  # Split the parent if it exceeds capacity

    def delete(self, key, node: Node = None):
        """
        Delete a key from the tree.
        :param key: The key to delete.
        :param node: The node to start deletion. If None, the correct node is located.
        """
        if node is None:
            node = self.find(key)  # Locate the node containing the key
        del node[key]  # Remove the key and associated value(s)

        if len(node.keys) < self.minimum:
            if node == self.root:
                # If the root is empty and has children, update the root
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]  # Update root to its first child
                    self.root.parent = None
                    self.depth -= 1  # Decrease tree depth
                return

            # Borrow a key or merge nodes if underutilized
            elif not node.borrow_key(self.minimum):
                node.fusion()  # Merge with a sibling
                self.delete(key, node.parent)  # Recursively clean up the parent

    def show(self, node=None, file=None, _prefix="", _last=True):
        """
        Print the tree structure, showing keys at each level.
        :param node: The node to start printing from. If None, start from the root.
        :param file: Optional file to write the output to.
        :param _prefix: Prefix for tree visualization.
        :param _last: Boolean indicating if the node is the last child.
        """
        if node is None:
            node = self.root
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # Recursively print the keys of child nodes
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.show(child, file, _prefix, _last)

    def output(self):
        """
        Return statistics about the tree structure.
        :return: A tuple containing the counts of splits, parent splits, fusions, and depth.
        """
        return splits, parent_splits, fusions, parent_fusions, self.depth

    def leftmost_leaf(self) -> Leaf:
        """
        Find the leftmost leaf in the tree.
        :return: The leftmost leaf node.
        """
        node = self.root
        while type(node) is not Leaf:
            node = node.values[0]  # Traverse to the first child
        return node


def demo():
    """
    Demonstrate the functionality of the B+ Tree.
    Inserts and deletes random keys, showing the tree structure at each step.
    """
    bplustree = BPlusTree()  # Create a new B+ Tree
    random_list = random.sample(range(1, 100), 20)  # Generate 20 random keys

    # Insert keys into the tree
    for i in random_list:
        bplustree[i] = 'test' + str(i)  # Insert key-value pairs
        print('Insert ' + str(i))
        bplustree.show()  # Show tree structure after each insertion

    random.shuffle(random_list)  # Shuffle the keys for deletion
    # Delete keys from the tree
    for i in random_list:
        print('Delete ' + str(i))
        bplustree.delete(i)  # Delete the key
        bplustree.show()  # Show tree structure after each deletion


if __name__ == '__main__':
    demo()  # Run the demo when the script is executed directly
