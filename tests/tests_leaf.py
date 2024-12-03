import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from leaf import Leaf  
from node import Node

class TestLeaf(unittest.TestCase):
    """Test suite for the Leaf class."""

    def setUp(self):
        """Set up reusable Leaf instances for testing."""
        self.leaf = Leaf()
        self.parent = Leaf()
        self.prev_leaf = Leaf()
        self.next_leaf = Leaf()

    def test_leaf_initialization(self):
        """Test leaf initialization and linking."""
        leaf = Leaf(parent=self.parent, prev_node=self.prev_leaf, next_node=self.next_leaf)
        self.assertEqual(leaf.parent, self.parent, "Leaf should have the correct parent.")
        self.assertEqual(leaf.prev, self.prev_leaf, "Leaf should be linked to the previous leaf.")
        self.assertEqual(leaf.next, self.next_leaf, "Leaf should be linked to the next leaf.")
        self.assertEqual(self.prev_leaf.next, leaf, "Previous leaf should link back to the current leaf.")
        self.assertEqual(self.next_leaf.prev, leaf, "Next leaf should link back to the current leaf.")

    def test_set_and_get_item(self):
        """Test setting and getting items in the leaf."""
        self.leaf['a'] = 'alpha'
        self.assertEqual(self.leaf['a'], 'alpha', "Leaf should store and retrieve the correct value.")

    def test_split_leaf(self):
        """Test splitting a leaf."""
        self.leaf.keys = ['a', 'b', 'c', 'd']
        self.leaf.values = ['alpha', 'bravo', 'charlie', 'delta']

        key, children = self.leaf.split()
        self.assertEqual(key, 'c', "The split key should be the middle key.")
        self.assertEqual(children[0].keys, ['a', 'b'], "Left child should contain the smaller half of the keys.")
        self.assertEqual(children[0].values, ['alpha', 'bravo'], "Left child should contain the corresponding values.")
        self.assertEqual(children[1].keys, ['c', 'd'], "Right child should contain the larger half of the keys.")
        self.assertEqual(children[1].values, ['charlie', 'delta'], "Right child should contain the corresponding values.")
        self.assertIsNotNone(children[0].next, "Left child should be linked to the right child.")
        self.assertEqual(children[0].next, children[1], "Left child's next should be the right child.")

    def test_delete_item(self):
        """Test deleting an item from the leaf."""
        self.leaf.keys = ['a', 'b', 'c']
        self.leaf.values = ['alpha', 'bravo', 'charlie']

        del self.leaf['b']
        self.assertEqual(self.leaf.keys, ['a', 'c'], "Key 'b' should be deleted.")
        self.assertEqual(self.leaf.values, ['alpha', 'charlie'], "Value 'bravo' should be deleted.")

    def test_fusion(self):
        """Test merging a leaf with its sibling."""
        self.leaf.keys = ['a', 'b']
        self.leaf.values = ['alpha', 'bravo']
        sibling = Leaf(prev_node=self.leaf)
        sibling.keys = ['c', 'd']
        sibling.values = ['charlie', 'delta']
        self.leaf.next = sibling

        self.leaf.fusion()

        self.assertEqual(self.leaf.keys, ['a', 'b', 'c', 'd'], "Keys should be merged.")
        self.assertEqual(self.leaf.values, ['alpha', 'bravo', 'charlie', 'delta'], "Values should be merged.")
        self.assertIsNone(self.leaf.next, "After fusion, there should be no next sibling.")


    def test_borrow_key(self):
        """Test borrowing a key from a sibling leaf."""
        self.leaf.keys = ['a']
        self.leaf.values = ['alpha']
        sibling = Leaf()
        sibling.keys = ['b', 'c']
        sibling.values = ['bravo', 'charlie']

        # Setup sibling and parent links
        self.leaf.next = sibling
        sibling.prev = self.leaf
        self.leaf.parent = Node()
        self.leaf.parent.keys = ['b']
        self.leaf.parent.values = [self.leaf, sibling]

        # Perform borrow operation
        self.assertTrue(self.leaf.borrow_key(1), "Borrowing a key should succeed.")
        self.assertEqual(self.leaf.keys, ['a', 'b'], "The borrowed key should be added.")
        self.assertEqual(self.leaf.values, ['alpha', 'bravo'], "The corresponding value should be added.")
        self.assertEqual(sibling.keys, ['c'], "The borrowed key should be removed from the sibling.")
        self.assertEqual(sibling.values, ['charlie'], "The corresponding value should be removed from the sibling.")
        self.assertEqual(self.leaf.parent.keys, ['c'], "Parent keys should be updated after borrowing.")


if __name__ == '__main__':
    unittest.main()
