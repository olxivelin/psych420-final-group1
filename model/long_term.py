from data_structures import BinarySearchTree


class LongTermMemory:

    def __init__(self):
        self._valence_tree = BinarySearchTree()
        self._dominance_tree = BinarySearchTree()
        self._arousal_tree = BinarySearchTree()
