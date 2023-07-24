from model.sensory import SensoryMemory


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensory = SensoryMemory("./data/BRM-emot-submit.csv")

    print(sensory.encode_input("cat"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
