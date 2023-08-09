from model.brain.brain import Brain
from collections import namedtuple, defaultdict
from enum import Enum, unique

import csv
import random


# TODO: add graph outputs for the recall percentages
#  compared with interference levels and time passed
#  maybe rehearsal frequency?


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
        self.max_ages = []
        self.rundus_results = []

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

        # for time, values in self.data_points[self.Category.STM][self.Action.FORGET]:
        #     # memory.original_value, memory.value, memory.age, memory.total_age
        #     series[values[0]]["xs"].append(time)
        #     series[values[0]]["ys"].append(0)
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

    def decayed_word_factors(self):
        series = defaultdict(lambda: defaultdict(list))

        for time, values in self.data_points[self.Category.STM][self.Action.STORE]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["valence"].append(values[1][0])
            series[values[0]]["arousal"].append(values[1][1])
            series[values[0]]["dominance"].append(values[1][2])

        for time, values in self.data_points[self.Category.STM][self.Action.ADJUST]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["valence"].append(values[1][0])
            series[values[0]]["arousal"].append(values[1][1])
            series[values[0]]["dominance"].append(values[1][2])

        for time, values in self.data_points[self.Category.STM][self.Action.FORGET]:
            # memory.original_value, memory.value, memory.age, memory.total_age
            series[values[0]]["xs"].append(time)
            series[values[0]]["valence"].append(0)
            series[values[0]]["arousal"].append(0)
            series[values[0]]["dominance"].append(0)

        return series

    def stash_rundus_results(self, results):
        self.rundus_results.append(results)

    def rundus_results_probabilities(self):
        remembered = [x[2] for x in self.rundus_results]

        num_words = len(remembered[0])
        num_trials = len(remembered)

        probs = []
        for i in range(num_words):
            total_remembered_at_i_across_trials = sum([x[i] for x in remembered])
            probs.append(total_remembered_at_i_across_trials / num_trials)

        return probs


class Simulation:

    def __init__(self, word_list=None):
        if word_list is None:
            word_list = ["person", "man", "woman", "camera", "tv", ]
        self.data_monitor = DataMonitor()
        self.brain = Brain(self.data_monitor)
        self._rehearsal_list = word_list

    def run_1(self, distraction_level=0.2, total_time=100, rehearsal_interval=10, fuzzy_threshold=0.03):
        self.brain.distraction_level = distraction_level
        self.brain.fuzzy_threshold = fuzzy_threshold

        for i in range(total_time):
            self.data_monitor.tick()
            self.brain.time_tick()

            rehearsal_index = i % rehearsal_interval
            if rehearsal_index < len(self.rehearsal_list):
                self.brain.rehearse(self.rehearsal_list[rehearsal_index])

        # self.data_monitor.log(f"Current Brain State: \n {self.brain}")
        # print(f"Current Brain State: \n {self.brain}")
        # for word_pairs in self.brain.remember(with_original=True):
        #     print("Recalled based on Short Term Memory")
        #     print(f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} \n")

        self.brain.end_simulation()
        self.data_monitor.print_log()

        return self.remember_from_ltm()
        # for i in range(1000):
        #     self.clock.tick()
        #     self.brain.time_tick(with_trace)
        #
        # # print(self.brain)
        # print(self.brain.remember(with_original=True))

    def run_2(self, distraction_level=0, total_time=20, fuzzy_threshold=0.03):
        self.brain.distraction_level = distraction_level
        self.brain.fuzzy_threshold = fuzzy_threshold

        # Load all the words for the trial
        for word in self.rehearsal_list:
            self.brain.rehearse(word)

        # Let time pass without rehearsing
        for i in range(0, total_time):
            self.data_monitor.tick()
            self.brain.time_tick()

        self.brain.end_simulation()
        self.data_monitor.print_log()

        return self.brain.recall(with_original=True)

    def recall_from_stm(self, with_original=True):
        return self.brain.recall(with_original=True)

    def remember_from_ltm(self, word_list=None):
        if word_list is None:
            word_list = self.rehearsal_list
        return self.brain.remember_from_ltm(word_list)

    def preload(self, data_file, brain=None):
        if brain is None:
            brain = self.brain
        with open(data_file, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)

            for word_data in word_reader:
                brain.preload(word_data["Word"],
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

    @property
    def stm_purge_strategy(self):
        return self.brain.hippocampus.short_term_memory.purge_strategy

    @stm_purge_strategy.setter
    def stm_purge_strategy(self, strategy):
        self.brain.hippocampus.short_term_memory.purge_strategy = strategy

    def random_words(self, number):
        return [random.choice(list(self.brain.cortex.sensory_memory.word_mapping.keys())) for i in range(number)]

    def run_rundus_inspired_trial(self, distraction_level=0, total_time=200,
                                  rehearsal_interval=5, fuzzy_threshold=0, max_words_per_second=4,
                                  rehearsal_strategy="oldest_first", brain=None):
        # 20 words (technically supposed to be nouns, but using words instead), presented for 5 seconds each.
        # 5 second interval between words, free to rehearse any word as long
        # as rehearsal filled the intervals. Recall the words in any order.

        if brain is None:
            brain = self.brain

        word_list = self.random_words(20)

        for word in word_list:
            # presentation interval
            for i in range(5):
                for j in range(random.randint(1, max_words_per_second)):
                    brain.rehearse(word)
                brain.time_tick()

            # rehearsal interval
            for i in range(5):
                stm_words = brain.hippocampus.short_term_memory.retrieve(False)
                for j in range(random.randint(1, max_words_per_second)):
                    brain.rehearse(brain.cortex.sensory_memory.decode(*stm_words[j % len(stm_words)]))
                brain.time_tick()

        recalled_words = brain.dump()

        remembered_items = [0] * len(word_list)
        for i in range(len(word_list)):
            if word_list[i] in recalled_words:
                remembered_items[i] = 1

        extra_items = len(recalled_words) - sum(remembered_items)

        return word_list, recalled_words, remembered_items, extra_items

    def run_rundus_inspired_experiment(self, data_file, trials=10):
        # run multiple trials

        for trial in range(trials):
            data_monitor = DataMonitor()
            brain = Brain(data_monitor)
            self.preload(data_file, brain=brain)
            self.data_monitor.stash_rundus_results(self.run_rundus_inspired_trial(brain=brain))

        return self.data_monitor.rundus_results
