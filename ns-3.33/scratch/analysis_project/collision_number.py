from transmission.CollisionDetector import CollisionDetector
from data_access.DataProvider import DataProvider

if __name__ == '__main__':

    provider = DataProvider('data/number_of_nanobots/results-300.csv')
    nanobots_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()

    all_records = []
    for nanobot_id in nanobots_map:
        records = nanobots_map[nanobot_id]
        for record in records:
            all_records.append(record)

    all_records.sort(key=lambda x: x.timestamp)

    detector = CollisionDetector(all_records, blood_vessels_map)
    for collision in detector.collisions:
        print(collision)
