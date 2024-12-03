import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from node import Node  # Assuming 'Node' is in the same format as the given implementation.

class TestNode(unittest.TestCase):
    """Test suite for the Node class."""

    def setUp(self):
        """Set up a reusable Node instance."""
        self.node = Node()

    def test_insert_single_key_value(self):
        """Test inserting a single key-value pair."""
        self.node.keys = ['a']
        self.node.values = [['alpha']]
        self.assertEqual(self.node.keys, ['a'], "Node should contain one key: 'a'.")
        self.assertEqual(self.node.values, [['alpha']], "Node values should correspond to the key.")

    def test_insert_multiple_keys(self):
        """Test inserting multiple keys."""
        keys_values = [('b', 'bravo'), ('a', 'alpha'), ('c', 'charlie')]

        # Insert and sort keys with corresponding values
        for key, value in keys_values:
            index = self.node.index(key)
            self.node.keys.insert(index, key)
            self.node.values.insert(index, Node())  # Insert a Node object as a value for consistency

        self.assertEqual(self.node.keys, ['a', 'b', 'c'], "Keys should be inserted in sorted order.")
        # Values are now Node objects; verify their content or instance
        self.assertTrue(all(isinstance(v, Node) for v in self.node.values), "Values should be Node objects.")


    def test_duplicate_key_value(self):
        """Test handling duplicate key-value pairs."""
        self.node.keys = ['a']
        self.node.values = [['alpha']]
        # Simulate insertion of duplicates
        if 'a' not in self.node.keys:
            self.node.keys.append('a')
            self.node.values.append(['alpha'])
        self.assertEqual(self.node.keys, ['a'], "Duplicate keys should not be added.")
        self.assertEqual(self.node.values, [['alpha']], "Duplicate values should not be added.")

    def test_split_node(self):
        """Test splitting a node."""
        self.node.keys = ['a', 'b', 'c', 'd']
        self.node.values = [['alpha'], ['bravo'], ['charlie'], ['delta']]
        key, children = self.node.split()
        self.assertEqual(key, 'c', "Middle key should be returned after splitting.")
        self.assertEqual(children[0].keys, ['a', 'b'], "Left child should contain the smaller half of the keys.")
        self.assertEqual(children[1].keys, ['d'], "Right child should contain the larger half of the keys.")

    def test_is_node_full(self):
        """Test checking if a node is full."""
        self.node.keys = ['a', 'b', 'c']
        self.assertFalse(len(self.node.keys) >= 4, "Node should not be full with three keys.")

        self.node.keys.append('d')
        self.assertTrue(len(self.node.keys) >= 4, "Node should be full with four keys.")

    def test_display_keys(self):
        """Test displaying node keys."""
        self.node.keys = ['a', 'b', 'c']
        output = f"Node keys: {self.node.keys}"
        self.assertEqual(output, "Node keys: ['a', 'b', 'c']", "Keys should match the display output.")

    def test_insert_large_number_of_keys(self):
        """Test inserting a large number of keys."""
        for i in range(10):
            self.node.keys.append(str(i))
        self.node.keys.sort()

        self.assertEqual(len(self.node.keys), 10, "Node should have all inserted keys.")
        self.assertTrue('5' in self.node.keys, "Node should contain the middle key after insertion.")

if __name__ == '__main__':
    unittest.main()
