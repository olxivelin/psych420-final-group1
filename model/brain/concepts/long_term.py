from .data_structures import Factor


class LongTermMemory:

    def __init__(self, data_monitor, fuzzy_threshold=0.03):
        self._valence_factor = Factor(data_monitor)
        self._dominance_factor = Factor(data_monitor)
        self._arousal_factor = Factor(data_monitor)
        self.data_monitor = data_monitor
        self.fuzzy_threshold = fuzzy_threshold

    def __str__(self):
        return f"Valence: \n {self._valence_factor} \n Arousal: \n {self._arousal_factor} \n Dominance: \n {self._dominance_factor}"

    def time_tick(self):
        pass

    def end_simulation(self):
        pass

    def set_fuzzy_threshold(self,  fuzzy_threshold):
        self.fuzzy_threshold = fuzzy_threshold
        self._valence_factor.set_fuzzy_threshold(fuzzy_threshold)
        self._dominance_factor.set_fuzzy_threshold(fuzzy_threshold)
        self._arousal_factor.set_fuzzy_threshold(fuzzy_threshold)

    def prime(self, data, valence, arousal, dominance):
        self._valence_factor.add_item(valence, data)
        self._dominance_factor.add_item(dominance, data)
        self._arousal_factor.add_item(arousal, data)

    def lookup(self, valence, arousal, dominance):
        valence_values = self._valence_factor.closest_matches(valence)
        arousal_values = self._arousal_factor.closest_matches(arousal)
        dominance_values = self._dominance_factor.closest_matches(dominance)
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))

    # def learn(self, word, valence, arousal, dominance):
    #     self.prime(word, valence, arousal, dominance)
    #     return self.lookup(valence, arousal, dominance)
    #
    # def feedback(self, word, valence, arousal, dominance, was_correct):
    #     self._valence_factor.adjust_weight(word, valence, was_correct)
    #     self._arousal_factor.adjust_weight(word, arousal, was_correct)
    #     self._dominance_factor.adjust_weight(word, dominance, was_correct)
