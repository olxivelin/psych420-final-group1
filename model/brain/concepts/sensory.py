import random


class SensoryMemory:

    def __init__(self, data_monitor):
        self.word_mapping = {}
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Encoding Map: \n {self.word_mapping}"

    def time_tick(self):
        pass

    def prime(self, word, valence, arousal, dominance):
        self.word_mapping[word] = (float(valence), float(arousal), float(dominance))

    def encode_input(self, sensed_input):
        return self.word_mapping.get(sensed_input)

    def decode(self, valence, arousal, dominance):
        """ Helper function purely for testing output"""
        for key, value in self.word_mapping.items():
            if value == (valence, arousal, dominance):
                return key

    def sense(self):
        word = random.choice(list(self.word_mapping.keys()))
        data = self.encode_input(word)
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
