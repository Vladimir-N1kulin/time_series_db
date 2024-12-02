import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from bplustree import BPlusTree


def test_insert():
    tree = BPlusTree(order=4)
    tree.insert(1, "value1")
    assert tree.search(1) == "value1"
