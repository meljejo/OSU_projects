# Name: Melissa J Johnson
# OSU Email: johnmel3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 BST/AVL Tree Implementation
# Due Date: 02/21/2022 + 1 free day
# Description:   Implement an AVL tree.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super().str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a node to the AVL tree. Duplicate values are not added.
        After addition, the tree is rebalanced if necessary.
        """
        if self.root is None:
            self.root = AVLNode(value)
        else:
            self._add(value, self.root)

    def _add(self, value, curr_node):
        """
        Recursively adds a new node to the AVL tree.
        :param value: value of the node to add
        :param curr_node: starts as self.root and then traverse down tree to
        find insertion.
        """
        if value == curr_node.value:
            return
        # Add to left when there is no left child
        if value < curr_node.value and curr_node.left is None:
            # Set left child to AVLNode(value)
            curr_node.left = AVLNode(value)
            # Update parent
            curr_node.left.parent = curr_node
            n = curr_node.left
            p = n.parent
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return

        # Add to right when there is no right child
        if value > curr_node.value and curr_node.right is None:
            curr_node.right = AVLNode(value)
            curr_node.right.parent = curr_node
            # Check balance
            n = curr_node.right
            p = n.parent
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return

        # Add to left side (when there is a left subtree). Recursively traverse
        # down tree to find insertion point.
        if value < curr_node.value and curr_node.left is not None:
            self._add(value, curr_node.left)
            return

        # Add to right side (when there is a right subtree). Recursively traverse
        # down tree to find insertion point.
        if value > curr_node.value and curr_node.right is not None:
            self._add(value, curr_node.right)
            return

    def remove(self, value: object) -> bool:
        """
        Removes a value from the AVL tree. If the value is present and removed, the method
        returns True, otherwise it returns False.
        """
        if self.is_empty():
            return False

        # Check that value is in the tree
        del_node = self.find(value)
        if del_node is None:
            return False

        del_node_children = self.num_children(del_node)

        # Case 1: No Children
        if del_node_children == 0:
            if del_node.parent is not None:
                # Delete reference to the node from parent
                if del_node.parent.left == del_node:
                    del_node.parent.left = None
                else:
                    del_node.parent.right = None
            else:
                # If del_node is the root node
                self.root = None

            p = del_node.parent
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return True

        # Case 2: Node has one child
        if del_node_children == 1:
            # Find child node
            if del_node.left is not None:
                child = del_node.left
            else:
                child = del_node.right

            if del_node.parent is not None:
                # Replace del_node with its child
                if del_node.parent.left == del_node:
                    del_node.parent.left = child
                else:
                    del_node.parent.right = child
            else:
                self.root = child

            # Correct pointers
            child.parent = del_node.parent
            p = del_node.parent
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return True


        # Case 3: When node has two children
        # Find inorder successor
        successor = self.min_value_node(del_node.right)

        if del_node_children == 2:
            # ap is the lowest modified node ('action position')
            ap = successor.parent
            # dnp is the deleted node parent
            dnp = del_node.parent
            # ks is successor parent
            ks = successor.parent

            # connect successor's left subtree with the deleted node's left subtree
            successor.left = del_node.left
            successor.left.parent = successor

            if successor is not del_node.right:
                ks.left = successor.right
                successor.right = del_node.right

                # The deleted node has been replaced with the successor.
                # Update successor's right child parent to be successor.
                if successor.right is not None:
                    successor.right.parent = successor

                # If successor parent (KS) left is successor's subtree:
                if ks.left is not None:
                    ks.left.parent = ks
                    ap = ap.left
            else:
                # Update the 'action position'
                ap = successor

            # If the root (del_node's parent) is being removed
            if dnp is None:
                self.root = successor
                successor.parent = None

            else:
                # Point parent of deleted node to point to inorder successor
                if dnp.right == del_node:
                    dnp.right = successor
                if dnp.left == del_node:
                    dnp.left = successor
                successor.parent = del_node.parent

            while ap is not None:
                self.rebalance(ap)
                ap = ap.parent
            return True


    def min_value_node(self, node):
        if node is None or node.left is None:
            return node
        else:
            return self.min_value_node(node.left)

    def num_children(self, node):
        num_children = 0
        if node.left is not None: num_children += 1
        if node.right is not None: num_children += 1
        return num_children

    # ------------------------------------------------------------------ #

    ################################################################
    # It's highly recommended, though not required,
    # to implement these methods for balancing the AVL Tree.
    ################################################################

    def get_height(self, node):
        if not node:
            return 0
        return self.get_height(node)

    def balance_factor(self, node):
        """
        This method calculates the balance factor of the node.
        The height of a null node (empty subtree) is -1.
        """

        if node.left is not None:
            lh_height = node.left.height
        else:
            lh_height = -1

        if node.right is not None:
            rh_height = node.right.height
        else:
            rh_height = -1

        return rh_height - lh_height

    def update_height(self, node):
        """
        This method updates the height of the node.
        """
        if node.left is not None:
            lh_height = node.left.height
        else:
            lh_height = -1

        if node.right is not None:
            rh_height = node.right.height
        else:
            rh_height = -1

        if rh_height > lh_height:
            max_height = rh_height + 1
        elif lh_height > rh_height:
            max_height = lh_height + 1
        else:
            max_height = rh_height + 1

        node.height = max_height

    def rotate_left(self, node):
        """
        This method performs a left rotation centered around 'node'.
        """
        c = node.right
        node.right = c.left
        if node.right is not None:
            node.right.parent = node
        c.left = node
        temp_parent = node.parent
        if temp_parent is None:
            self.root = c
        c.parent = temp_parent
        node.parent = c
        self.update_height(node)
        # Update height after subtree was restructured
        self.update_height(c)
        # Return the new root of the subtree at which the rotation was performed
        return c

    def rotate_right(self, node):
        """
        This method performs a right rotation centered around 'node.'
        """
        c = node.left
        node.left = c.right
        if node.left is not None:
            node.left.parent = node

        c.right = node
        temp_parent = node.parent
        if temp_parent is None:
            self.root = c
        c.parent = temp_parent
        node.parent = c
        self.update_height(node)
        self.update_height(c)
        # Return the new root of the subtree at which the rotation was performed
        return c

    def rebalance(self, node):
        """
        This method performs rebalancing at each node.
        The inner statements check if double rotation is needed by checking
        if n's child is imbalanced in the opposite direction of n's imbalance.
        """

        balance_factor = self.balance_factor(node)

        if balance_factor < -1:
            if self.balance_factor(node.left) > 0:
                # First rotation of double rotation. Rotate around node's
                # child and update parent.
                node.left = self.rotate_left(node.left)
                node.left.parent = node
            new_subtree_root = self.rotate_right(node)
            if new_subtree_root.parent is not None:
                if new_subtree_root.parent.left is node:
                    new_subtree_root.parent.left = new_subtree_root
                if new_subtree_root.parent.right is node:
                    new_subtree_root.parent.right = new_subtree_root

        if balance_factor > 1:
            if self.balance_factor(node.right) < 0:
                # First rotation of double rotation. Rotate around node's child
                # and update parent
                node.right = self.rotate_right(node.right)
                node.right.parent = node
            new_subtree_root = self.rotate_left(node)
            if new_subtree_root.parent is not None:
                if new_subtree_root.parent.right is node:
                    new_subtree_root.parent.right = new_subtree_root
                if new_subtree_root.parent.left is node:
                    new_subtree_root.parent.left = new_subtree_root

        # No rotation is performed, but update node's subtree height
        else:
            self.update_height(node)

    def find(self, value):
        """
        Method that finds a value in the AVL tree.
        """
        return self._find(value, self.root)


    def _find(self, value, node):
        """
        Recursive function to traverse down the tree to find a node (if present) in the tree.
        """

        if value == node.value:
            return node
        if value < node.value and node.left is None:
            return None
        if value > node.value and node.right is None:
            return None
        if value < node.value:
            return self._find(value, node.left)
        if value > node.value:
            return self._find(value, node.right)

    # ------------------------------------------------------------------ #

    ################################################################
    # Use the methods as a starting point if you'd like to override.
    # Otherwise, the AVL can simply call any BST method.
    ################################################################

    '''
    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        return super().contains(value)

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        return super().inorder_traversal()

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        return super().find_min()

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        return super().find_max()

    def is_empty(self) -> bool:
        """
        TODO: Write your implementation
        """
        return super().is_empty()

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        super().make_empty()
    '''


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),  # RR, RR
        (10, 20, 30, 50, 40),  # RR, RL
        (30, 20, 10, 5, 1),  # LL, LL
        (30, 20, 10, 1, 5),  # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', tree, tree.root.value)
        tree.remove(tree.root.value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
