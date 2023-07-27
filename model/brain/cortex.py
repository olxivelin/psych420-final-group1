from .concepts.long_term import LongTermMemory
from .concepts.sensory import SensoryMemory


class Cortex:

    def __init__(self):
        self.sensory_memory = SensoryMemory()
        self.long_term_memory = LongTermMemory()

    def __str__(self):
        return f"Sensory Memory: \n {self.sensory_memory} \n Long Term Memory: \n {self.long_term_memory} \n"

    def preload(self, word, valence, arousal, dominance):
        self.sensory_memory.prime(word, valence, arousal, dominance)
        # self.long_term_memory.prime(word, valence, arousal, dominance)

    def time_tick(self, with_trace):
        self.sensory_memory.time_tick(with_trace)
        self.long_term_memory.time_tick(with_trace)

    def sense(self):
        return self.sensory_memory.sense()

    def store_memory(self, memory):
        # TODO: should we do something with the strength, age at the point we
        # are transferring from short term to long term memory
        meaning = self.sensory_memory.decode(*memory.original_value)
        self.long_term_memory.prime(meaning, *memory.value)

    def retrieve_memory(self, valence, arousal, dominance):
        return self.long_term_memory.lookup(valence, arousal, dominance)
