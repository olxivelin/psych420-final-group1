from random import random, randint

class MemoryRegister:

    def __init__(self, value, age):
        self.original_value = value
        self.value = value
        self.age = age

    def __str__(self):
        return f"Age: {self.age} Value: {self.value} Original: {self.original_value}"


class ShortTermMemory:

    def __init__(self):
        self.registers = []

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
        for memory in self.registers:
            memory.age += 1
            memory.value = self.fuzz(memory)
            if memory.age >= self.current_max_duration():
                forget.append(memory)

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
            if memory.value == value:
                exists = True
                memory.age = 0

        if not exists:
            self.registers.append(MemoryRegister(value, 0))

        # if we have too many items then remove the oldest item.
        self.potentially_forget_oldest(with_trace)

    def retrieve(self, with_original):
        if with_original:
            return [memory.value for memory in self.registers], [memory.original_value for memory in self.registers]
        return [memory.value for memory in self.registers]

    def fuzz(self, memory):
        fuzz_factor = 1 / ((self.current_max_duration() - memory.age) or 1) ** 2
        return memory.value[0] + fuzz_factor, memory.value[1] + fuzz_factor, memory.value[2] + fuzz_factor
