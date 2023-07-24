import csv


def train(data_file, long_term_memory):

    with open(data_file, newline='') as csvfile:
        word_reader = csv.DictReader(csvfile)

        for word_data in word_reader:
            long_term_memory.prime(word_data["Word"],
                                   word_data["Valence"],
                                   word_data["Dominance"],
                                   word_data["Arousal"])
