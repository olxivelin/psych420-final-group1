from simulation import Simulation

# Example of running
if __name__ == '__main__':
    simulation = Simulation()
    # simulation.preload("./data/test.csv")
    simulation.preload("./data/BRM-emot-submit.csv")
    simulation.run_1()

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
