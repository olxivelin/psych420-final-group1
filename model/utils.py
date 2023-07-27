import csv

#TODO: This could maybe move into the memory models as a "learn" function?


def train(data_file, long_term_memory):

    # TODO: Rather than just priming LTM directly, build a back prop
    # method to update the weights (and thresholds?)
    with open(data_file, newline='') as csvfile:
        word_reader = csv.DictReader(csvfile)

        for word_data in word_reader:
            long_term_memory.prime(word_data["Word"],
                                   float(word_data["Valence"]),
                                   float(word_data["Arousal"]),
                                   float(word_data["Dominance"]),
                                   )
