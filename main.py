from model.sensory import SensoryMemory
from model.long_term import LongTermMemory
from model.utils import train

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensory = SensoryMemory("./data/BRM-emot-submit.csv")

    ltm = LongTermMemory()
    train("./data/BRM-emot-submit.csv", ltm)

    ltm.print()

    data = sensory.encode_input("cat")
    print(data)

    print(ltm.lookup(*data))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
