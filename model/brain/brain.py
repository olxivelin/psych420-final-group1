from .cortex import Cortex
from .hippocampus import Hippocampus
from random import random


class Brain:

    def __init__(self, data_monitor, distraction_level=0.2):
        self.cortex = Cortex(data_monitor)
        self.hippocampus = Hippocampus(self.cortex, data_monitor)
        self.distraction_level = distraction_level
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Cortex: \n {self.cortex} \n Hippocampus: \n {self.hippocampus} \n"

    def set_distraction_level(self, distraction_level):
        self.distraction_level = distraction_level

    def time_tick(self):

        self.hippocampus.time_tick()
        self.cortex.time_tick()

        if random() < self.distraction_level:
            self.hippocampus.process_sensory_input(self.cortex.sense())

    def preload(self, word, valence, arousal, dominance):
        self.cortex.preload(word, valence, arousal, dominance)

    def rehearse(self, word):
        sensory_input = self.cortex.sensory_memory.encode_input(word)
        self.data_monitor.log(f"Rehearsing {sensory_input}")
        self.data_monitor.add_data_point(self.data_monitor.Category.STM, self.data_monitor.Action.REHEARSE, word)
        self.hippocampus.short_term_memory.add(sensory_input)

    def remember(self, with_original):
        words = []
        short_term_memory_contents, original_values, strengths = self.hippocampus.short_term_memory.retrieve(with_original)
        for i in range(len(short_term_memory_contents)):
            orig_valence, orig_arousal, orig_dominance = original_values[i]
            original_word = self.cortex.sensory_memory.decode(orig_valence, orig_arousal, orig_dominance)
            valence, arousal, dominance = short_term_memory_contents[i]
            remembered_word = self.cortex.long_term_memory.lookup(valence, arousal, dominance)
            if remembered_word:
                words.append([original_word, remembered_word, strengths[i]])
        return words
