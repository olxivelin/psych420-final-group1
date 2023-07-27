# TODO: add the concept of time passing and have items age out of short term memory.

class ShortTermMemory:

    def __init__(self, ltm):
        self.registers = []
        self.long_term_memory = ltm

    def add(self, value):
        # if it is already in sort term memory then remove it and add it to the end of the list.
        if value in self.registers:
            self.registers.remove(value)

        self.registers.append(value)

        # if we have too many items then remove the oldest item.
        if len(self.registers) > 7:
            self.registers.pop(0)

    def fuzz(self, valence, arousal, dominance):
        index = self.registers.index((valence, arousal, dominance))
        # TODO: I just picked a random equation here, is there something better to do here?
        fuzz_factor = (len(self.registers) - index - 1) / len(self.registers) ** 2.5
        return valence + fuzz_factor, arousal + fuzz_factor, dominance + fuzz_factor

    def retrieve_from_long_term(self, valence, arousal, dominance):
        values = self.fuzz(valence, arousal, dominance)
        return self.long_term_memory.lookup(*values)

    def print(self):
        for item in self.registers:
            print(f"Item {item} with fuzz factor {self.fuzz(*item)}")

    def learn(self, word, encoded_word):
        self.add(encoded_word)
        return self.long_term_memory.learn(word, *encoded_word)

    def feedback(self, word, encoded_word, was_correct):
        self.long_term_memory.feedback(word, *encoded_word, was_correct)
