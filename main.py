from model.sensory import SensoryMemory
from model.short_term import ShortTermMemory
from model.long_term import LongTermMemory
from model.utils import train

# Example of running
if __name__ == '__main__':
    ltm = LongTermMemory()
    stm = ShortTermMemory(ltm)
    sensory = SensoryMemory("./data/BRM-emot-submit.csv", stm)

    for word in sensory.word_mapping.keys():
        sensory.learn(word)

    # train("./data/BRM-emot-submit.csv", ltm)
    # ltm.print()

    # data = sensory.encode_input("cat")
    # print(data)
    # print(ltm.lookup(*data))

    for i in range(7):
        sensory.sense()

    for item in stm.registers:
        recovered_memory = stm.retrieve_from_long_term(*item)
        print(recovered_memory)
