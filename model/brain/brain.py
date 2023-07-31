from .cortex import Cortex
from .hippocampus import Hippocampus
from random import random


class Brain:

    def __init__(self, data_monitor, distraction_level=0.2, fuzzy_threshold=0.03):
        self.cortex = Cortex(data_monitor)
        self.hippocampus = Hippocampus(self.cortex, data_monitor)
        self.distraction_level = distraction_level
        self.fuzzy_threshold = fuzzy_threshold
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Cortex: \n {self.cortex} \n Hippocampus: \n {self.hippocampus} \n"

    def set_distraction_level(self, distraction_level):
        self.distraction_level = distraction_level

    def set_fuzzy_threshold(self,  fuzzy_threshold):
        self.fuzzy_threshold = fuzzy_threshold
        self.cortex.set_fuzzy_threshold(fuzzy_threshold)

    def time_tick(self):

        self.hippocampus.time_tick()
        self.cortex.time_tick()

        if random() < self.distraction_level:
            self.hippocampus.process_sensory_input(self.cortex.sense())

    def end_simulation(self):
        self.hippocampus.end_simulation()
        self.cortex.end_simulation()

    def preload(self, word, valence, arousal, dominance):
        self.cortex.preload(word, valence, arousal, dominance)

    def rehearse(self, word):
        sensory_input = self.cortex.sensory_memory.encode(word)
        self.data_monitor.log(f"Rehearsing {sensory_input}")
        self.data_monitor.add_data_point(self.data_monitor.Category.STM, self.data_monitor.Action.REHEARSE, word)
        self.hippocampus.short_term_memory.add(sensory_input)

    def remember_from_ltm(self, word_list):
        found = []
        for word in word_list:
            encoded_word = self.cortex.sensory_memory.encode(word)
            remembered_word = self.cortex.long_term_memory.lookup(*encoded_word)
            if remembered_word:
                found.append(remembered_word)
        return found

    def recall(self, with_original):
        words = []
        short_term_memory_contents, original_values, strengths = self.hippocampus.short_term_memory.retrieve(with_original)
        for i in range(len(short_term_memory_contents)):
            orig_valence, orig_arousal, orig_dominance = original_values[i]
            original_word = self.cortex.sensory_memory.decode(orig_valence, orig_arousal, orig_dominance)
            valence, arousal, dominance = short_term_memory_contents[i]
            recalled_word = self.cortex.fuzzy_lookup(valence, arousal, dominance)
            if recalled_word:
                words.append([original_word, recalled_word, strengths[i]])
        return words
