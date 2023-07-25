# Used to look for data that are near the value we have.
FUZZ_THRESHOLD = 0.1


class Node:
    def __init__(self, value=None, data=None):
        self.left = None
        self.right = None
        self.value = value
        self.data = []
        if data:
            self.data.append(data)

    def insert(self, value, data):
        if not self.value:
            self.value = value
            self.data.append(data)
            return

        if self.value == value:
            self.data.append(data)
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
        self.data = min_larger_node.data

        self.right = self.right.delete(min_larger_node.value)
        return self

    def find(self, value):
        if value == self.value:
            return self.data

        if value < self.value:
            if self.left is None:
                return None
            return self.left.find(value)

        if self.right is None:
            return None
        return self.right.find(value)

    def find_in_range(self, min_value, max_value):
        if self.value is None:
            return
        if min_value <= self.value <= max_value:
            left_values = []
            right_values = []
            if self.left is not None:
                left_values = self.left.find_in_range(min_value, max_value) or []
            if self.right is not None:
                right_values = self.right.find_in_range(min_value, max_value) or []
            return left_values + ([[self.data, self.value]] or []) + right_values

        if min_value < self.value:
            if self.left is not None:
                return self.left.find_in_range(min_value, max_value)

        if max_value > self.value:
            if self.right is not None:
                return self.right.find_in_range(min_value, max_value)

    def inorder(self, values):
        if self.left is not None:
            self.left.inorder(values)
        if self.value is not None:
            values.append(self.data)
        if self.right is not None:
            self.right.inorder(values)
        return values


class BinarySearchTree:

    def __init__(self):
        self.root = Node()

    def add(self, value, data):
        self.root.insert(value, data)

    def remove(self, value):
        self.root.delete(value)

    def find(self, value):
        return self.root.find(value)

    def fuzzy_find(self, value):
        return self.root.find_in_range(value - FUZZ_THRESHOLD, value + FUZZ_THRESHOLD)

    def print(self):
        print(self.root.inorder([]))
