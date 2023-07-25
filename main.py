from model.sensory import SensoryMemory
from model.short_term import ShortTermMemory
from model.long_term import LongTermMemory
from model.utils import train

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ltm = LongTermMemory()
    stm = ShortTermMemory(ltm)
    sensory = SensoryMemory("./data/BRM-emot-submit.csv", stm)

    train("./data/BRM-emot-submit.csv", ltm)
    ltm.print()

    # data = sensory.encode_input("cat")
    # print(data)
    # print(ltm.lookup(*data))

    for i in range(1):
        sensory.sense()

    # stm.print()

    # last_item = stm.registers[-1]

    for item in stm.registers:
        recovered_memory = stm.retrieve_from_long_term(*item)
        print(recovered_memory)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
