

class Node:
    def __init__(self, value=None, data=None):
        self.left = None
        self.right = None
        self.value = value
        self.data = data

    def insert(self, value, data):
        if not self.value:
            self.value = value
            self.data = data
            return

        if self.value == value:
            return

        if value < self.value:
            if self.left:
                self.left.insert(value, data)
                return
            self.left = Node(value, data)
            return

        if self.right:
            self.right.insert(value, data)
            return
        self.right = Node(value, data)

    def delete(self, value):
        if self is None:
            return self
        if value < self.value:
            self.left = self.left.delete(value)
            return self
        if value > self.value:
            self.right = self.right.delete(value)
            return self
        if self.right is None:
            return self.left
        if self.left is None:
            return self.right
        min_larger_node = self.right
        while min_larger_node.left:
            min_larger_node = min_larger_node.left
        self.value = min_larger_node.value
        self.right = self.right.delete(min_larger_node.value)
        return self

    def find(self, value):
        if value == self.value:
            return self.data

        if value < self.value:
            if self.left is None:
                return None
            return self.left.exists(value)

        if self.right is None:
            return None
        return self.right.exists(value)


class BinarySearchTree:

    def __init__(self):
        self.root = Node()

    def add(self, value, data):
        self.root.insert(value, data)

    def remove(self, value):
        self.root.delete(value)
