from .concepts.short_term import ShortTermMemory


class Hippocampus:

    def __init__(self):
        self.short_term_memory = ShortTermMemory()

    def __str__(self):
        return f"Short Term Memory: \n {self.short_term_memory} \n"

    def time_tick(self, with_trace):
        self.short_term_memory.time_tick(with_trace)

    def process_sensory_input(self, sensory_input, with_trace):
        self.short_term_memory.add(sensory_input, with_trace)
