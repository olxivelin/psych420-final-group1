from .cortex import Cortex
from .hippocampus import Hippocampus
from random import random


# TODO: Caroline picked a random number here, is there data we should be using?
PROBABILITY_OF_ATTENDING = 0.2


class Brain:

    def __init__(self):
        self.cortex = Cortex()
        self.hippocampus = Hippocampus(self.cortex)

    def __str__(self):
        return f"Cortex: \n {self.cortex} \n Hippocampus: \n {self.hippocampus} \n"

    def time_tick(self, with_trace):

        self.hippocampus.time_tick(with_trace)
        self.cortex.time_tick(with_trace)

        if random() < PROBABILITY_OF_ATTENDING:
            self.hippocampus.process_sensory_input(self.cortex.sense(), with_trace)

    def preload(self, word, valence, arousal, dominance):
        self.cortex.preload(word, valence, arousal, dominance)

    def rehearse(self, word, with_trace):
        sensory_input = self.cortex.sensory_memory.encode_input(word)
        self.hippocampus.short_term_memory.add(sensory_input, with_trace)

    def remember(self, with_original):
        words = []
        short_term_memory_contents, original_values, strengths = self.hippocampus.short_term_memory.retrieve(with_original)
        for i in range(len(short_term_memory_contents)):
            orig_valence, orig_arousal, orig_dominance = original_values[i]
            original_word = self.cortex.sensory_memory.decode(orig_valence, orig_arousal, orig_dominance)
            valence, arousal, dominance = short_term_memory_contents[i]
            remembered_word = self.cortex.long_term_memory.lookup(valence, arousal, dominance) or "?"
            words.append([original_word, remembered_word, strengths[i]])
        return words
