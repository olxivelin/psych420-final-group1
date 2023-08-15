from simulation import Simulation

# Example of running
if __name__ == '__main__':
    print("Simulation 1")

    simulation1 = Simulation()
    simulation1.preload("./data/BRM-emot-submit.csv")
    results = simulation1.run_1()

    print(results)

    print("Simulation 2")

    simulation2 = Simulation()
    simulation2.preload("./data/BRM-emot-submit.csv")
    results = simulation2.run_2()
    print(results)

    print("Simulation 3")

    simulation3 = Simulation()
    simulation3.preload("./data/BRM-emot-submit.csv")
    results = simulation3.run_rundus_inspired_experiment("./data/BRM-emot-submit.csv", trials=10)

    for result in results:
        word_list, recalled_words, remembered_items, extra = result
        print(f"Word List {word_list}")
        print(f"Recalled List {recalled_words}")
        print(f"Remembered: {remembered_items}")
        print(f"Extra Words: {extra}")
