import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from bplustree import BPlusTree
from node import Node

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.bplustree = BPlusTree(order=4)
        self.node = Node(order=4)

    def test_demo_node(self):
        print('Initializing node...')
        node = self.node

        print('\nInserting key a...')
        node.insert_key_value('a', 'alpha')
        print('Is node full?', node.is_node_full())
        node.display_keys()

        print('\nInserting keys b, c, d...')
        node.insert_key_value('b', 'bravo')
        node.insert_key_value('c', 'charlie')
        node.insert_key_value('d', 'delta')
        print('Is node full?', node.is_node_full())
        node.display_keys()

        print('\nSplitting node...')
        node.split_node()
        node.display_keys()

    def test_demo_bplustree(self):
        print('Initializing B+ tree...')
        bplustree = self.bplustree

        print('\nB+ tree with 1 item...')
        bplustree.insert_key_value('a', 'alpha')
        bplustree.display_tree()

        print('\nB+ tree with 2 items...')
        bplustree.insert_key_value('b', 'bravo')
        bplustree.display_tree()

        print('\nB+ tree with 3 items...')
        bplustree.insert_key_value('c', 'charlie')
        bplustree.display_tree()

        print('\nB+ tree with 4 items...')
        bplustree.insert_key_value('d', 'delta')
        bplustree.display_tree()

        print('\nB+ tree with 5 items...')
        bplustree.insert_key_value('e', 'echo')
        bplustree.display_tree()

        print('\nB+ tree with 6 items...')
        bplustree.insert_key_value('f', 'foxtrot')
        bplustree.display_tree()

        print('\nRetrieving values with key e...')
        print(bplustree.retrieve_value('e'))

if __name__ == '__main__':
    unittest.main()
