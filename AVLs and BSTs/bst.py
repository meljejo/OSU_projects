# Name: Melissa J Johnson
# OSU Email: johnmel3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 BST/AVL Tree Implementation
# Due Date: 02/21/2022 + 1 free day
# Description:   Implement a BST and AVL tree.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of BST in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self.str_helper(self.root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self.str_helper(node.left, values)
        self.str_helper(node.right, values)

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree. Duplicate values are added to the
        right subtree.
        """
        if self.root is None:
            self.root = BSTNode(value)
        else:
            self._add(value, self.root)  #Private 'add' is recursive

    def _add(self, value, current_node):
        if value < current_node.value:
            if current_node.left is None:  #If current_node doesn't have left child
                current_node.left = BSTNode(value)
            else:
                self._add(value, current_node.left)   #If current_node does have a left child
        elif value >= current_node.value:
            if current_node.right is None:
                current_node.right = BSTNode(value)
            else:
                self._add(value, current_node.right)


    def remove(self, value: object) -> bool:
        """
        This method removes a value from the tree. If the value is removed, the method
        returns True, otherwise it returns False.
        """
        # If the tree is empty
        if self.root is None:
            return False

        # If the node to be deleted is the root node
        elif self.root.value == value:
            # If the tree is a one node tree, delete the root
            if self.root.left is None and self.root.right is None:
                self.root = None
            # If the root node only has left child
            elif self.root.left and self.root.right is None:
                self.root = self.root.left
            # If the root node only has right child
            elif self.root.left is None and self.root.right:
                self.root = self.root.right

            # If the root node has both left and right children
            elif self.root.left and self.root.right:
                parent_of_deleted_node = self.root
                deleted_node = self.root.right
                while deleted_node.left:
                    parent_of_deleted_node = deleted_node
                    deleted_node = deleted_node.left

                if deleted_node.right:
                    if parent_of_deleted_node.value > deleted_node.value:
                        parent_of_deleted_node.left = deleted_node.right

                    # <= makes sure that the value further down the tree is deleted after copying. Adding this note
                    # for myself since I spent far too long debugging.
                    elif parent_of_deleted_node.value <= deleted_node.value:
                        parent_of_deleted_node.right = deleted_node.right

                else:
                    if deleted_node.value < parent_of_deleted_node.value:
                        parent_of_deleted_node.left = None
                    else:
                        parent_of_deleted_node.right = None

                self.root.value = deleted_node.value

            return True

        # This is the code for non-empty trees and the data is not in the root node
        parent = None
        node = self.root

        # First find the node to remove
        while node and node.value != value:
            parent = node
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right

        # If node is not in tree
        if node is None or node.value != value:
            return False

        # If the node to remove is a leaf node
        elif node.left is None and node.right is None:
            if value < parent.value:
                parent.left = None
            else:
                parent.right = None
            return True

        # Remove node that does not have right child
        elif node.left and node.right is None:
            if value < parent.value:
                parent.left = node.left
            else:
                parent.right = node.left
            return True

        # Remove node that does not have left child
        elif node.left is None and node.right:
            if value < parent.value:
                parent.left = node.right
            else:
                parent.right = node.right
            return True

        # Remove a node with two children
        else:
            parent_of_del_node = node
            del_node = node.right
            # while loop to find the lowest value in the right subtree
            while del_node.left:
                parent_of_del_node = del_node
                del_node = del_node.left

            # copy value once node has been found
            node.value = del_node.value
            if del_node.right:
                if parent_of_del_node.value > del_node.value:
                    parent_of_del_node.left = del_node.right

                    # Same note as code for root node (~Line 133) that the
                    # <= sign is to insure that once the del_node value is copied
                    # to the node.value, that the value further down the tree is deleted
                elif parent_of_del_node.value <= del_node.value:
                    parent_of_del_node.right = del_node.right
            else:
                if del_node.value < parent_of_del_node.value:
                    parent_of_del_node.left = None
                else:
                    parent_of_del_node.right = None
            return True

    def contains(self, value: object) -> bool:
        """
        This method returns True if the value is in the tree
        and returns False if the value is not in the tree.
        """
        if self.root is not None:
            return self._contains(value, self.root)
        else:
            return False

    def _contains(self, value, current_node):
        """
        Recursive method to determine if value is in the BST.
        """
        if value == current_node.value:
            return True
        elif value < current_node.value and current_node.left is not None:
            return self._contains(value, current_node.left)
        elif value > current_node.value and current_node.right is not None:
            return self._contains(value, current_node.right)
        return False

    def inorder_traversal(self) -> Queue:
        """
        This method performs an inorder traversal of the tree and returns
        a Queue object that contains the node values in the order of the traversal.
        """
        result_queue = Queue()
        if self.is_empty():
            return result_queue
        else:
            return self._inorder_traversal(self.root, result_queue)

    def _inorder_traversal(self, current_node, rec_queue):
        """
        Recursive method to perform the inorder traversal of the BST. Returns
        the inorder traversal as a Queue object.
        """
        if current_node is not None:
            self._inorder_traversal(current_node.left, rec_queue)
            rec_queue.enqueue(current_node.value)
            self._inorder_traversal(current_node.right, rec_queue)
        return rec_queue

    def find_min(self) -> object:
        """
        This methods finds the lowest value in the tree and returns it. It works
        by recursively traversing the node from the root to the left. Once a node
        is found which has a NULL left value, the minimum has been found.
        If the tree is empty, the method returns None.
        """

        if self.root is not None:
            return self._find_min(self.root)
        else:
            return None

    def _find_min(self, current_node):
        if current_node.left is None:
            return current_node.value
        return self._find_min(current_node.left)

    def find_max(self) -> object:
        """
        This method finds the largest value in the tree and returns it. If the tree
        is empty, the method returns None.
        """
        if self.root is not None:
            return self._find_max(self.root)
        else:
            return None

    def _find_max(self, current_node):
        if current_node.right is None:
            return current_node.value
        return self._find_max(current_node.right)

    def is_empty(self) -> bool:
        """
        This method checks if the tree is empty. If the the tree is empty, the
        method returns True, otherwise it returns False.
        """
        if self.root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        This method removes all nodes from the tree.
        """
        self.root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 1,5")
    print("-------------------------------")
    case = (32, 34, -29, 37, 10, 13, -45, 85, -39, -65)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(32)
        print('RESULT :', tree)
        tree.remove(-29)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 1,6")
    print("-------------------------------")
    case = (15, 1, -13, -19, 15, -3, 18, 6, 16, -16, -11, -16, -9, 6,
            -17, 5, -4, 2, 6, -7, 7, -9, 9, -2, 20, 15, 1, 2, 6, -12)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(-20)
        tree.remove(-19)
        tree.remove(10)
        tree.remove(-18)
        tree.remove(-12)
        tree.remove(9)
        tree.remove(-20)
        tree.remove(5)
        tree.remove(-16)
        tree.remove(-10)
        tree.remove(-17)
        tree.remove(-14)
        tree.remove(-4)
        tree.remove(15)
        print('RESULT :', tree)


    print("\nPDF - method remove() example 1,75")
    print("-------------------------------")
    case = (32, -96, 70, -24, -82, 14, -44, -73, 62, -34)

    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(32)
        print('RESULT :', tree)
        tree.remove(70)
        print('RESULT :', tree)
        tree.remove(-82)
        print('RESULT :', tree)


    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        print('INPUT  :', tree, tree.root.value)
        tree.remove(tree.root.value)
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
