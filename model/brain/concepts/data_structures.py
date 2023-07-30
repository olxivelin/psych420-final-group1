

# TODO: not sure about this, it is being used to allow multiple value lists to be returned if
# they are all within the threshold amount.
ERROR_THRESHOLD = 0.08


class Node:
    def __init__(self, data_monitor, value, data):
        self.left = None
        self.right = None
        self.value = value
        self.data = []
        if data:
            self.data.append(data)
        self.data_monitor = data_monitor

    def insert(self, value, data):
        if not self.value:
            self.value = value
            if data not in self.data:
                self.data.append(data)
            return

        if self.value == value:
            if data not in self.data:
                self.data.append(data)
            return

        if value < self.value:
            if self.left:
                self.left.insert(value, data)
                return
            self.left = Node(self.data_monitor, value, data)
            return

        if self.right:
            self.right.insert(value, data)
            return
        self.right = Node(self.data_monitor, value, data)

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
            values.append([self.value, self.data])
        if self.right is not None:
            self.right.inorder(values)
        return values


class BinarySearchTree:

    def __init__(self, data_monitor, fuzzy_threshold=0.03):
        self.root = Node(data_monitor, None, None)
        self.fuzzy_threshold = fuzzy_threshold

    def __str__(self):
        return f"{self.root.inorder([])}"

    def set_fuzzy_threshold(self,  fuzzy_threshold):
        self.fuzzy_threshold = fuzzy_threshold

    def add(self, value, data):
        self.root.insert(value, data)

    def remove(self, value):
        self.root.delete(value)

    def find(self, value):
        return self.root.find(value)

    def fuzzy_find(self, value):
        return self.root.find_in_range(value - self.fuzzy_threshold, value + self.fuzzy_threshold)


class Factor:
    def __init__(self, data_monitor, fuzzy_threshold=0.03):
        self._tree = BinarySearchTree(data_monitor)
        self._weight = 1
        self.data_monitor = data_monitor
        self.fuzzy_threshold = fuzzy_threshold

    def __str__(self):
        return f"Weight: {self._weight} \n Tree: {self._tree}"

    def set_fuzzy_threshold(self, fuzzy_threshold):
        self.fuzzy_threshold = fuzzy_threshold

    def get_error(self, item, value):
        # TODO: pretty sure I'm not using weight the way we want to here.
        error = abs((item[1] - value) * self._weight)
        return error

    def add_item(self, value, data):
        self._tree.add(value, data)

    def closest_matches(self, value):
        values = self._tree.fuzzy_find(value) or [[], 0]

        closest_matches = []
        for item in values:
            if item:
                if self.get_error(item, value) <= ERROR_THRESHOLD:
                    closest_matches += item[0]
        return closest_matches


    def adjust_weight(self, word, value, was_correct):
        # TODO: This should likely be using something other than a fixed value.
        matches = self.closest_matches(value)
        if word in matches:
            self._weight += 0.0001
        else:
            if not was_correct:
                self._weight -= 0.0001
