from .data_structures import BinarySearchTree

# TODO: not sure about this, it is being used to allow multiple value lists to be returned if
# they are all within the threshold amount.
ERROR_THRESHOLD = 0.08


class Factor:
    def __init__(self):
        self._tree = BinarySearchTree()
        self._weight = 1

    def __str__(self):
        return f"Weight: {self._weight} \n Tree: {self._tree}"

    def get_error(self, item, value):
        #TODO: pretty sure I'm not using weight the way we want to here.
        error = abs((item[1] - value) * self._weight)
        # print(error)
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


class LongTermMemory:

    def __init__(self):
        self._valence_factor = Factor()
        self._dominance_factor = Factor()
        self._arousal_factor = Factor()

    def __str__(self):
        return f"Valence: \n {self._valence_factor} \n Arousal: \n {self._arousal_factor} \n Dominance: \n {self._dominance_factor}"

    def time_tick(self, with_trace):
        pass

    def prime(self, data, valence, arousal, dominance):
        self._valence_factor.add_item(valence, data)
        self._dominance_factor.add_item(dominance, data)
        self._arousal_factor.add_item(arousal, data)

    def lookup(self, valence, arousal, dominance):
        valence_values = self._valence_factor.closest_matches(valence)
        arousal_values = self._arousal_factor.closest_matches(arousal)
        dominance_values = self._dominance_factor.closest_matches(dominance)
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))

    def learn(self, word, valence, arousal, dominance):
        self.prime(word, valence, arousal, dominance)
        return self.lookup(valence, arousal, dominance)

    def feedback(self, word, valence, arousal, dominance, was_correct):
        self._valence_factor.adjust_weight(word, valence, was_correct)
        self._arousal_factor.adjust_weight(word, arousal, was_correct)
        self._dominance_factor.adjust_weight(word, dominance, was_correct)
