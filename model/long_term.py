from .data_structures import BinarySearchTree

# TODO: not sure about this, it is being used to allow multiple value lists to be returned if
# they are all within the threshold amount.
ERROR_THRESHOLD = 0.1


class Factor:
    def __init__(self):
        self._tree = BinarySearchTree()
        self._weight = 1

    def get_error(self, item, value):
        #TODO: pretty sure I'm not using weight the way we want to here.
        error = abs((item[1] - value) * self._weight)
        # print(error)
        return error

    def add_item(self, value, data):
        self._tree.add(value, data)

    def print(self):
        self._tree.print()

    def closest_matches(self, value):
        values = self._tree.fuzzy_find(value) or [[], 0]
        # values.sort(key=lambda x: self.get_error(x, value))

        closest_matches = []
        for item in values:
            if self.get_error(item, value) <= ERROR_THRESHOLD:
                closest_matches += item[0]
        # print(f"Closest Matches: {closest_matches}")
        return closest_matches


class LongTermMemory:

    def __init__(self):
        self._valence_factor = Factor()
        self._dominance_factor = Factor()
        self._arousal_factor = Factor()

    def prime(self, data, valance, dominance, arousal):
        self._valence_factor.add_item(valance, data)
        self._dominance_factor.add_item(dominance, data)
        self._arousal_factor.add_item(arousal, data)

    def print(self):
        self._valence_factor.print()
        self._dominance_factor.print()
        self._arousal_factor.print()

    def lookup(self, valence, arousal, dominance):
        valence_values = self._valence_factor.closest_matches(valence)
        # print(f"Valence: {valence_values}")
        arousal_values = self._arousal_factor.closest_matches(arousal)
        # print(f"Arousal: {arousal_values}")
        dominance_values = self._dominance_factor.closest_matches(dominance)
        # print(f"Dominance: {dominance_values}")
        # print("Intersection of valence and arousal")
        # print(set(valence_values).intersection(set(arousal_values)))
        # print("Intersection of dominance and arousal")
        # print(set(arousal_values).intersection(set(dominance_values)))
        # print("Intersection of valence and dominance")
        # print(set(valence_values).intersection(set(dominance_values)))
        # print("Intersection of valence and arousal and dominance")
        # print(set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values)))
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))
