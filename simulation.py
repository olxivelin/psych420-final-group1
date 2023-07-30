from model.brain.brain import Brain
from collections import namedtuple, defaultdict
from enum import Enum, unique

import csv


# TODO: add graph outputs for the recall percentages
#  compared with interference levels and time passed
#  maybe rehearsal frequency?

class MonitorableMixin:
    def __init__(self):
        self.data_monitor = None

    def set_trace_monitor(self, data_monitor):
        self.data_monitor = data_monitor


class DataMonitor:
    @unique
    class Category(Enum):
        STM_TO_LTM = "stm-to-ltm"
        STM = "stm"

    class Action(Enum):
        STORE = "store"
        FORGET = "forget"
        ADJUST = "adjust"
        REHEARSE = "rehearse"

    def __init__(self):
        self.elapsed_time = 0
        self.trace_log_lines = []
        self.data_points = defaultdict(lambda: defaultdict(list))

    def tick(self):
        self.elapsed_time += 1

    def log(self, trace):
        self.trace_log_lines.append(trace)

    def add_data_point(self, category, action, value):
        self.data_points[category][action].append([self.elapsed_time, value])

    def print_log(self):
        for line in self.trace_log_lines:
            print(line)

    def data_for_decay_factors(self):
        series = defaultdict(lambda: defaultdict(list))

        for time, values in self.data_points[self.Category.STM][self.Action.ADJUST]:
            # memory.original_value, memory.value, memory.age, memory.total_age, fuzz_factor
            series[values[0]]["xs"].append(time)
            series[values[0]]["ys"].append(values[4])

        for time, values in self.data_points[self.Category.STM][self.Action.FORGET]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["ys"].append(0)
        return series

    def rehearsal_points(self):
        series = defaultdict(lambda: defaultdict(list))

        for time, value in self.data_points[self.Category.STM][self.Action.REHEARSE]:
            # memory.original_value, memory.value
            series[value]["xs"].append(time)
            series[value]["ys"].append(1)

        return series

    def word_age(self):
        series = defaultdict(lambda: defaultdict(list))

        for time, values in self.data_points[self.Category.STM][self.Action.STORE]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["ys"].append(values[3])

        for time, values in self.data_points[self.Category.STM][self.Action.ADJUST]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["ys"].append(values[3])

        for time, values in self.data_points[self.Category.STM][self.Action.FORGET]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["ys"].append(0)

        return series


class Simulation:

    def __init__(self, word_list=["person", "man", "woman", "camera", "tv", ]):
        self.data_monitor = DataMonitor()
        self.brain = Brain(self.data_monitor)
        self._rehearsal_list = word_list

    def run_1(self, distraction_level=0.2, total_time=100):
        self.brain.set_distraction_level(distraction_level)

        rehearsal_rate = 10

        for i in range(total_time):
            self.data_monitor.tick()
            self.brain.time_tick()

            rehearsal_index = i % rehearsal_rate
            if rehearsal_index < len(self.rehearsal_list):
                self.brain.rehearse(self.rehearsal_list[rehearsal_index])

        # self.data_monitor.log(f"Current Brain State: \n {self.brain}")
        # print(f"Current Brain State: \n {self.brain}")
        # for word_pairs in self.brain.remember(with_original=True):
        #     print("Recalled based on Short Term Memory")
        #     print(f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} \n")

        self.data_monitor.print_log()

        return self.brain.remember(with_original=True)
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

    def lookup_word_from_encoding(self, encoding):
        return self.brain.cortex.sensory_memory.decode(*encoding)

    @property
    def rehearsal_list(self):
        return self._rehearsal_list

    @rehearsal_list.setter
    def rehearsal_list(self, value):
        self._rehearsal_list = value
