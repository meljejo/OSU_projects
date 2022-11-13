import unittest
from bst import *
from avl import AVL, AVLNode


class BSTTests(unittest.TestCase):
    def test_bst_node_init(self):
        bst_node = BSTNode(54)
        self.assertEqual(bst_node.left, None)
        self.assertEqual(bst_node.right, None)
        self.assertEqual(bst_node.value, 54)

    def test_add_node(self):
        bst = BST()
        bst.add(60)
        self.assertEqual(bst.root.value, 60)
        bst.add(58)
        self.assertEqual(bst.root.left.value, 58)
        # print(bst)

    def test_add_test_tree_and_remove(self):
        bst = BST()
        bst.add(32)
        bst.add(-96)
        bst.add(70)
        bst.add(-24)
        bst.add(-82)
        bst.add(14)
        bst.add(-44)
        bst.add(-73)
        bst.add(62)
        bst.add(-34)
        print(bst)
        bst.remove(32)
        print(bst)
        bst.remove(70)
        print(bst)
        bst.remove(-82)
        print(bst)

class AVLTests(unittest.TestCase):
    def test_avl_init(self):
        avl = AVL()
        avl.add(10)
        self.assertEqual(avl.root.value, 10)

    def test_avl_get_height(self):
        avl = AVL()
        avl.add(10)
        self.assertEqual(avl.get_height(), 0)

    def test_root_node_children(self):
        avl = AVL()
        self.assertIsNone(avl.root)
        avl.add(10)
        self.assertIsNotNone(avl.root)
        self.assertIsNone(avl.root.right)
        self.assertIsNone(avl.root.left)
        self.assertEqual(0, avl.get_height())

    def test_height_function(self):
        avl = AVL()
        self.assertEqual(0, avl.get_height())
        avl.add(10)
        self.assertEqual(0, avl.get_height())
        avl.add(15)
        self.assertEqual(1, avl.get_height())
        avl.add(20)
        self.assertEqual(2, avl.get_height())
        avl.add(8)
        avl.add(6)
        self.assertEqual(2, avl.get_height())
        avl.add(4)
        self.assertEqual(3, avl.get_height())

    def test_balance_factor(self):
        avl = AVL()
        self.assertEqual(0, avl.get_height())
        avl.add(10)
        self.assertEqual(0, avl.get_height())
        avl.add(15)
        self.assertEqual(1, avl.get_height())
        node = AVLNode(20)
        avl.add(20)
        node_bf = avl.balance_factor(node)
        #self.assertEqual(2, node_bf)
        print(avl.balance_factor(node))

