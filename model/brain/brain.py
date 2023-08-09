from .cortex import Cortex
from .hippocampus import Hippocampus
from random import random


class Brain:

    def __init__(self, data_monitor, distraction_level=0.2, fuzzy_threshold=0.03):
        self.cortex = Cortex(data_monitor)
        self.hippocampus = Hippocampus(self.cortex, data_monitor)
        self._distraction_level = distraction_level
        self._fuzzy_threshold = fuzzy_threshold
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Cortex: \n {self.cortex} \n Hippocampus: \n {self.hippocampus} \n"

    @property
    def distraction_level(self):
        return self._distraction_level

    @distraction_level.setter
    def distraction_level(self, distraction_level):
        self._distraction_level = distraction_level

    @property
    def fuzzy_threshold(self):
        return self._fuzzy_threshold

    @fuzzy_threshold.setter
    def fuzzy_threshold(self,  fuzzy_threshold):
        self._fuzzy_threshold = fuzzy_threshold
        self.cortex.fuzzy_threshold = fuzzy_threshold
        self.hippocampus.fuzzy_threshold = fuzzy_threshold

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
            if encoded_word:
                remembered_word = self.cortex.long_term_memory.lookup(*encoded_word)
                if remembered_word:
                    found.append(remembered_word)
        return found

    def recall(self, with_original):
        words = []
        if with_original:
            short_term_memory_contents, original_values, strengths = self.hippocampus.short_term_memory.retrieve(with_original)
            for i in range(len(short_term_memory_contents)):
                orig_valence, orig_arousal, orig_dominance = original_values[i]
                original_word = self.cortex.sensory_memory.decode(orig_valence, orig_arousal, orig_dominance)
                valence, arousal, dominance = short_term_memory_contents[i]
                recalled_word = self.cortex.fuzzy_lookup(valence, arousal, dominance)
                if recalled_word:
                    words.append([original_word, recalled_word, strengths[i]])
        else:
            short_term_memory_contents= self.hippocampus.short_term_memory.retrieve(with_original)
            for i in range(len(short_term_memory_contents)):
                valence, arousal, dominance = short_term_memory_contents[i]
                recalled_word = self.cortex.fuzzy_lookup(valence, arousal, dominance)
                if recalled_word:
                    for word in recalled_word:
                        words.append(word)
        return words

    def dump(self):
        # output everything in short and long term memory
        contents_of_stm = set(self.recall(False))
        contents_of_ltm = self.cortex.long_term_memory.retrieve()

        return contents_of_stm.union(contents_of_ltm)
