
import csv


class SensoryMemory:

    def __init__(self, word_file):
        self.word_mapping = {}
        self._load_data(word_file)

    def _load_data(self, word_file):
        with open(word_file, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)
            for word_data in word_reader:
                self.word_mapping[word_data["Word"]] = word_data

    def encode_input(self, sensed_input):
        found = self.word_mapping.get(sensed_input)
        if found:
            return found["Valence"], found["Arousal"], found["Dominance"]
