from .data_structures import BinarySearchTree


class LongTermMemory:

    def __init__(self):
        self._valence_tree = BinarySearchTree()
        self._dominance_tree = BinarySearchTree()
        self._arousal_tree = BinarySearchTree()

    def prime(self, data, valance, dominance, arousal):
        self._valence_tree.add(valance, data)
        self._dominance_tree.add(dominance, data)
        self._arousal_tree.add(arousal, data)

    def print(self):
        self._valence_tree.print()
        self._arousal_tree.print()
        self._dominance_tree.print()

    def lookup(self, valence, arousal, dominance):
        print(f"Inside lookup {valence}, {arousal}, {dominance}")

        valence_values = self._valence_tree.find(valence)
        arousal_values = self._arousal_tree.find(arousal)
        dominance_values = self._dominance_tree.find(dominance)
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))
