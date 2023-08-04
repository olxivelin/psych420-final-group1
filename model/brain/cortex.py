from .concepts.long_term import LongTermMemory
from .concepts.sensory import SensoryMemory


class Cortex:

    def __init__(self, data_monitor, fuzzy_threshold=0.03):
        self.sensory_memory = SensoryMemory(data_monitor)
        self.long_term_memory = LongTermMemory(data_monitor)
        self.data_monitor = data_monitor
        self._fuzzy_threshold = fuzzy_threshold

    def __str__(self):
        return f"Sensory Memory: \n {self.sensory_memory} \n Long Term Memory: \n {self.long_term_memory} \n"

    @property
    def fuzzy_threshold(self):
        return self._fuzzy_threshold

    @fuzzy_threshold.setter
    def fuzzy_threshold(self, fuzzy_threshold):
        self._fuzzy_threshold = fuzzy_threshold
        self.long_term_memory.fuzzy_threshold = fuzzy_threshold
        self.sensory_memory.fuzzy_threshold = fuzzy_threshold

    def preload(self, word, valence, arousal, dominance):
        self.sensory_memory.prime(word, valence, arousal, dominance)
        # self.long_term_memory.prime(word, valence, arousal, dominance)

    def time_tick(self):
        self.sensory_memory.time_tick()
        self.long_term_memory.time_tick()

    def end_simulation(self):
        self.sensory_memory.end_simulation()
        self.long_term_memory.end_simulation()

    def sense(self):
        return self.sensory_memory.sense()

    def store_memory(self, memory):
        # TODO: should we do something with the strength, age at the point we
        # are transferring from short term to long term memory
        meaning = self.sensory_memory.decode(*memory.original_value)
        self.data_monitor.log(f"Storing Meaning {meaning}, values {memory.value}")
        self.long_term_memory.prime(meaning, *memory.value)

    def retrieve_memory(self, valence, arousal, dominance):
        return self.long_term_memory.lookup(valence, arousal, dominance)

    def fuzzy_lookup(self, valence, arousal, dominance):
        return self.sensory_memory.fuzzy_lookup(valence, arousal, dominance)
