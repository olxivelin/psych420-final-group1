import csv
import random


class SensoryMemory:

    def __init__(self, word_file, stm):
        self.word_mapping = {}
        self._load_data(word_file)
        self.short_term_memory = stm

    def _load_data(self, word_file):
        with open(word_file, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)
            for word_data in word_reader:
                self.word_mapping[word_data["Word"]] = word_data

    def encode_input(self, sensed_input):
        found = self.word_mapping.get(sensed_input)
        if found:
            return float(found["Valence"]), float(found["Arousal"]), float(found["Dominance"])

    def sense(self):
        word = random.choice(list(self.word_mapping.keys()))
        print(f"Adding {word} to stm.")
        data = self.encode_input(word)
        self.short_term_memory.add(data)
