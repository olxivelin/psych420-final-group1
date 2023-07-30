from model.brain.brain import Brain
import csv


class Clock:

    def __init__(self):
        self.elapsed_time = 0

    def tick(self):
        self.elapsed_time += 1

# TODO: add graph outputs for the recall percentages
#  compared with interference levels and time passed
#  maybe rehearsal frequency?


class Simulation:

    def __init__(self):
        self.brain = Brain()
        self.clock = Clock()

    def run(self):

        with_trace = True

        rehearsal_rate = 10

        rehearsal_list = ["person", "man", "woman", "camera", "tv", ]
        for i in range(1000):
            self.clock.tick()
            self.brain.time_tick(with_trace)

            rehearsal_index = i % rehearsal_rate
            if rehearsal_index < len(rehearsal_list):
                self.brain.rehearse(rehearsal_list[rehearsal_index], with_trace)

        print(self.brain)
        for word_pairs in self.brain.remember(with_original=True):
            print("Recalled based on Short Term Memory")
            print(f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} \n")

        # for i in range(1000):
        #     self.clock.tick()
        #     self.brain.time_tick(with_trace)
        #
        # # print(self.brain)
        # print(self.brain.remember(with_original=True))

    def preload(self, data_file):
        with open(data_file, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)

            for word_data in word_reader:
                self.brain.preload(word_data["Word"],
                                   float(word_data["Valence"]),
                                   float(word_data["Arousal"]),
                                   float(word_data["Dominance"]),
                                   )
