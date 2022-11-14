import matplotlib.pyplot as plt

from transmission.CollisionDetector import CollisionDetector
from data_access.DataProvider import DataProvider

# Scenario 3
if __name__ == '__main__':

    nanobots_numbers = [100 * (i+2) for i in range(7)]
    results = []

    for number in nanobots_numbers:
        provider = DataProvider("../data/number_of_nanobots/results-{}.csv".format(number))
        records = [record for record in provider.nanobot_records if record.is_from_nanobot_to_access_point()]
        blood_vessels_map = provider.get_blood_vessels_map()
        detector = CollisionDetector(records, blood_vessels_map)
        results.append(len(detector.collisions) / len(records))

    ys = [result * 100 for result in results]
    figure, axis = plt.subplots()
    axis.set_xlabel("Number of nanobots")
    axis.set_ylabel("Collision ratio [collisions/transmissions] in %")
    axis.scatter(nanobots_numbers, ys, c='black')
    axis.set_title("Collision ratio as function of number of nanobots")
    plt.show()

