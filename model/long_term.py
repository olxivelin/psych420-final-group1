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
        #TODO: implememnt a fuzzy find where if an exact match isn't found it looks for values close enough
        valence_values = self._valence_tree.fuzzy_find(valence) or []
        # print(valence_values)
        arousal_values = self._arousal_tree.fuzzy_find(arousal) or []
        # print(arousal_values)
        dominance_values = self._dominance_tree.fuzzy_find(dominance) or []
        # print(dominance_values)
        # print("Intersection of valence and arousal")
        # print(set(valence_values).intersection(set(arousal_values)))
        # print("Intersection of dominance and arousal")
        # print(set(arousal_values).intersection(set(dominance_values)))
        # print("Intersection of valence and dominance")
        # print(set(valence_values).intersection(set(dominance_values)))
        # print("Intersection of valence and arousal and dominance")
        # print(set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values)))
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))
