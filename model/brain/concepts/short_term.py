from random import random, randint

# TODO: find a value that makes sense for this, what does the research say?
STRENGTH_THRESHOLD = 5  # how strong the memory in stm has to be before it is moved to LTM
STRENGTH_BOOST = 2  # how much to boost the strength if this is an item already in LTM
STRENGTH_INCREMENT = 1  # how much to increase strength each time an item already in STM is added again

# TODO: Rate of decay -> should be rapid for first 18 seconds - Peterson and Peterson (1959)
#  https://psycnet-apa-org.proxy.lib.uwaterloo.ca/fulltext/1960-05499-001.pdf
#  exponential decay perhaps?


class MemoryRegister:

    def __init__(self, value, age, strength, data_monitor):
        self.original_value = value
        self.value = value
        self.age = age
        self.total_age = age
        self.strength = strength
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Age: {self.total_age} Age since last Rehearsal: {self.age} Strength: {self.strength} " \
               f"Value: {self.value} Original: {self.original_value}"


class ShortTermMemory:

    def __init__(self, hippocampus, data_monitor):
        self.registers = []
        self.hippocampus = hippocampus
        self.data_monitor = data_monitor

    def __str__(self):
        return f"Registers: \n {[str(r) for r in self.registers]} \n"

    # Based on Miller's Magical Number Seven
    # https://journals-scholarsportal-info.proxy.lib.uwaterloo.ca/details/0033295x/v101i0002/343_tmnspooocfpi.xml
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

    def time_tick(self):
        """ Remove the memories that have been in stm too long"""
        forget = []
        store = []
        for memory in self.registers:
            memory.age += 1
            memory.total_age += 1
            memory.value = self.fuzz(memory)
            if memory.age >= self.current_max_duration():
                forget.append(memory)
            if memory.strength >= STRENGTH_THRESHOLD:
                store.append(memory)

        for memory in store:
            self.data_monitor.add_data_point(category=self.data_monitor.Category.STM_TO_LTM,
                                             action=self.data_monitor.Action.STORE,
                                             value=[memory.original_value, memory.value, memory.age, memory.total_age])
            self.data_monitor.log(f"Item going to long term memory: {memory}")
            self.hippocampus.send_to_long_term_storage(memory)

        for memory in forget:
            self.data_monitor.add_data_point(category=self.data_monitor.Category.STM,
                                             action=self.data_monitor.Action.FORGET,
                                             value=[memory.original_value, memory.value, memory.age, memory.total_age])
            self.data_monitor.log(f"Item too old forgetting {memory}\n")
            self.registers.remove(memory)

    def potentially_forget_oldest(self):
        max_quantity = self.current_max_capacity()
        if len(self.registers) > max_quantity:
            self.registers.sort(key=lambda x: x.age)
            for r in self.registers[max_quantity:]:
                self.data_monitor.add_data_point(category=self.data_monitor.Category.STM,
                                                 action=self.data_monitor.Action.FORGET,
                                                 value=[r.original_value, r.value, r.age, r.total_age])
                self.data_monitor.log(f"Too many items forgetting {str(r)}")
            self.registers = self.registers[0:max_quantity]

    def add(self, value):
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
            if value:
                existing_memory = self.hippocampus.retrieve_from_long_term_storage(*value)
                if existing_memory:
                    strength = STRENGTH_BOOST
                    self.data_monitor.log(f"Item {value} recognized, boosting strength")

                self.registers.append(MemoryRegister(value, 0, strength, self.data_monitor))

        # if we have too many items then remove the oldest item.
        self.potentially_forget_oldest()

    def retrieve(self, with_original):
        if with_original:
            return [memory.value for memory in self.registers], [memory.original_value for memory in self.registers], [memory.strength for memory in self.registers]
        return [memory.value for memory in self.registers]

    def fuzz(self, memory):
        max_duration = self.current_max_duration()

        # TODO: Adjust this factor to be more realistic. Find data.
        fuzz_factor = (1 / ((max_duration - memory.age) or 1) ** 2)
        self.data_monitor.add_data_point(
            category=self.data_monitor.Category.STM,
            action=self.data_monitor.Action.ADJUST,
            value=[memory.original_value, memory.value, memory.age, memory.total_age, fuzz_factor]
        )
        return memory.value[0] + fuzz_factor, memory.value[1] + fuzz_factor, memory.value[2] + fuzz_factor
