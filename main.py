from simulation import Simulation

# Example of running
if __name__ == '__main__':
    simulation = Simulation()
    # simulation.preload("./data/test.csv")
    simulation.preload("./data/BRM-emot-submit.csv")
    results = simulation.run_rundus_inspired_experiment("./data/BRM-emot-submit.csv", trials=10)

    for result in results:
        word_list, recalled_words, remembered_items, extra = result
        print(f"Word List {word_list}")
        print(f"Recalled List {recalled_words}")
        print(f"Remembered: {remembered_items}")
        print(f"Extra Words: {extra}")

    # print(simulation.data_monitor.data_for_decay_factors())
    # ltm = LongTermMemory()
    # stm = ShortTermMemory(ltm)
    # # sensory = SensoryMemory("./data/BRM-emot-submit.csv", stm)
    # sensory = SensoryMemory("./data/test.csv", stm)
    #
    # for i in range(100):
    #     for word in sensory.word_mapping.keys():
    #         sensory.learn(word)
    #
    # # train("./data/BRM-emot-submit.csv", ltm)
    # ltm.print()
    #
    #
    # # data = sensory.encode_input("cat")
    # # print(data)
    # # print(ltm.lookup(*data))
    #
    # for i in range(7):
    #     sensory.sense()
    #
    # # stm.print()
    #
    # for item in stm.registers:
    #     recovered_memory = stm.retrieve_from_long_term(*item)
    #     print(recovered_memory)
