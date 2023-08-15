import random
from .data_structures import Factor


class SensoryMemory:

    def __init__(self, data_monitor, fuzzy_threshold=0.03):
        # We have a list of all the words that we can sense
        # so that we know what to process on "sensing".
        self.word_mapping = {}
        # We've also added the tree representation to Sensory Memory so that we
        # could do fuzzy lookups without re-implementing. It seems like a
        # hacky thing to do.
        self._valence_factor = Factor(data_monitor)
        self._dominance_factor = Factor(data_monitor)
        self._arousal_factor = Factor(data_monitor)

        # data monitor is for simulation purposes to be able to log
        # as processing happens.
        self.data_monitor = data_monitor

        # fuzzy threshold is a dial that can be tweaked in the simulation
        # to indicate how much drift will interfere with lookups.
        self._fuzzy_threshold = fuzzy_threshold

    def __str__(self):
        return f"Encoding Map: \n {self.word_mapping}"

    def time_tick(self):
        pass

    def end_simulation(self):
        pass

    @property
    def fuzzy_threshold(self):
        return self._fuzzy_threshold

    @fuzzy_threshold.setter
    def fuzzy_threshold(self, fuzzy_threshold):
        self._fuzzy_threshold = fuzzy_threshold
        self._valence_factor.fuzzy_threshold = fuzzy_threshold
        self._dominance_factor.fuzzy_threshold = fuzzy_threshold
        self._arousal_factor.fuzzy_threshold = fuzzy_threshold

    def prime(self, word, valence, arousal, dominance):
        self._valence_factor.add_item(float(valence), word)
        self._dominance_factor.add_item(float(dominance), word)
        self._arousal_factor.add_item(float(arousal), word)
        self.word_mapping[word] = (float(valence), float(arousal), float(dominance))

    def encode(self, sensed_input):
        return self.word_mapping.get(sensed_input)

    def decode(self, valence, arousal, dominance):
        """ Helper function purely for testing output"""
        for key, value in self.word_mapping.items():
            if value == (valence, arousal, dominance):
                return key

    def fuzzy_lookup(self, valence, arousal, dominance):
        valence_values = self._valence_factor.closest_matches(valence)
        arousal_values = self._arousal_factor.closest_matches(arousal)
        dominance_values = self._dominance_factor.closest_matches(dominance)
        return set(valence_values).intersection(set(arousal_values)).intersection(set(dominance_values))

    def sense(self):
        word = random.choice(list(self.word_mapping.keys()))
        data = self.encode(word)
        return data

    # def learn(self, word):
    #     encoded = self.encode_input(word)
    #     self.short_term_memory.add(encoded)
    #     retrieved = self.short_term_memory.retrieve_from_long_term(*encoded)
    #     if word not in retrieved:
    #         retrieved = self.short_term_memory.learn(word, encoded)
    #     correct = word in retrieved
    #     self.feedback(word, correct)
    #
    # def feedback(self, word, was_correct):
    #     encoded = self.encode_input(word)
    #     self.short_term_memory.feedback(word, encoded, was_correct)
