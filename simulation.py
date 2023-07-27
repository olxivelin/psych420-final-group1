from model.brain.brain import Brain
import csv


class Clock:

    def __init__(self):
        self.elapsed_time = 0

    def tick(self):
        self.elapsed_time += 1


class Simulation:

    def __init__(self):
        self.brain = Brain()
        self.clock = Clock()

    def run(self):

        with_trace = True

        for i in range(1000):
            self.clock.tick()
            self.brain.time_tick(with_trace)

        # print(self.brain)
        print(self.brain.remember(with_original=True))

        for i in range(1000):
            self.clock.tick()
            self.brain.time_tick(with_trace)

        # print(self.brain)
        print(self.brain.remember(with_original=True))

    def preload(self, data_file):
        with open(data_file, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)

            for word_data in word_reader:
                self.brain.preload(word_data["Word"],
                                   float(word_data["Valence"]),
                                   float(word_data["Arousal"]),
                                   float(word_data["Dominance"]),
                                   )
