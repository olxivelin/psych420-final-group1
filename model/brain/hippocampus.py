from .concepts.short_term import ShortTermMemory


class Hippocampus:

    def __init__(self, cortex):
        self.cortex = cortex
        self.short_term_memory = ShortTermMemory(self)

    def __str__(self):
        return f"Short Term Memory: \n {self.short_term_memory} \n"

    def time_tick(self, with_trace):
        self.short_term_memory.time_tick(with_trace)

    def process_sensory_input(self, sensory_input, with_trace):
        self.short_term_memory.add(sensory_input, with_trace)

    def send_to_long_term_storage(self, memory):
        self.cortex.store_memory(memory)

    def retrieve_from_long_term_storage(self, valence, arousal, dominance):
        return self.cortex.retrieve_memory(valence, arousal, dominance)
