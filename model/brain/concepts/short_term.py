from random import random, randint

# TODO: find a value that makes sense for this, what does the research say?
STRENGTH_THRESHOLD = 5  # how strong the memory in stm has to be before it is moved to LTM
STRENGTH_BOOST = 2  # how much to boost the strength if this is an item already in LTM
STRENGTH_INCREMENT = 1  # how much to increase strength each time an item already in STM is added again

# TODO: Rate of decay -> should be rapid for first 18 seconds - Peterson and Peterson (1959)
#  https://psycnet-apa-org.proxy.lib.uwaterloo.ca/fulltext/1960-05499-001.pdf
#  exponential decay perhaps?
class MemoryRegister:

    def __init__(self, value, age, strength):
        self.original_value = value
        self.value = value
        self.age = age
        self.strength = strength

    def __str__(self):
        return f"Age: {self.age} Strength: {self.strength} Value: {self.value} Original: {self.original_value}"


class ShortTermMemory:

    def __init__(self, hippocampus):
        self.registers = []
        self.hippocampus = hippocampus

    def __str__(self):
        return f"Registers: \n {[str(r) for r in self.registers]} \n"

    @staticmethod
    def current_max_capacity():
        """Return a value between 7 +/- 2"""
        extra = randint(-2, 2)
        return 7 + extra

    @staticmethod
    def current_max_duration():
        """Return a value between 15 - 30"""
        extra = random() * 15
        return 15 + extra

    def time_tick(self, with_trace):
        """ Remove the memories that have been in stm too long"""
        forget = []
        store = []
        for memory in self.registers:
            memory.age += 1
            memory.value = self.fuzz(memory)
            if memory.age >= self.current_max_duration():
                forget.append(memory)
            if memory.strength >= STRENGTH_THRESHOLD:
                store.append(memory)

        for memory in store:
            if with_trace:
                print(f"Item going to long term memory: {memory}")
            self.hippocampus.send_to_long_term_storage(memory)

        for memory in forget:
            if with_trace:
                print(f"Item too old forgetting {memory}\n")
            self.registers.remove(memory)

    def potentially_forget_oldest(self, with_trace):
        max_quantity = self.current_max_capacity()
        if len(self.registers) > max_quantity:
            self.registers.sort(key=lambda x: x.age)

            if with_trace:
                print(f"Too many items forgetting {[str(r) for r in self.registers[max_quantity:]]}")
            self.registers = self.registers[0:max_quantity]

    def add(self, value, with_trace):
        # if it is already in sort term memory reset the age.
        exists = False
        for memory in self.registers:
            # TODO: since we're storing the fuzzed value in memory.value I had to change
            #  this to compare with original_value, which isn't what we want to do,
            #  this likely needs to do a fuzzy match similar to the LTM look up rather than
            #  an exact match like this, and then we can compare to memory.value.
            if memory.original_value == value:
                exists = True
                memory.age = 0
                memory.strength += STRENGTH_INCREMENT  # The more you see something the stronger the memory

        if not exists:
            # see if memory is already in long term memory and boost strength
            # to mimic the idea of it being easier to remember things you know -
            # TODO: find data to back this up. Right now Caroline *thinks* she read this,
            #  but isn't 100% sure.
            strength = 0
            existing_memory = self.hippocampus.retrieve_from_long_term_storage(*value)
            if existing_memory:
                strength = STRENGTH_BOOST
                if with_trace:
                    print("Item recognized, boosting strength")

            self.registers.append(MemoryRegister(value, 0, strength))

        # if we have too many items then remove the oldest item.
        self.potentially_forget_oldest(with_trace)

    def retrieve(self, with_original):
        if with_original:
            return [memory.value for memory in self.registers], [memory.original_value for memory in self.registers], [memory.strength for memory in self.registers]
        return [memory.value for memory in self.registers]

    def fuzz(self, memory):
        fuzz_factor = 1 / ((self.current_max_duration() - memory.age) or 1) ** 2
        return memory.value[0] + fuzz_factor, memory.value[1] + fuzz_factor, memory.value[2] + fuzz_factor
