import matplotlib.pyplot as plt
import numpy as np

from model.DataPacket import DataPacket
from data_access.DataProvider import DataProvider
from transmission.CollisionDetector import CollisionDetector
from transmission.TransmissionSimulator import TransmissionSimulator

# Scenario 2
if __name__ == '__main__':

    test_size = 100
    nanobot_numbers = [1000 * (i+1) for i in range(100)]

    flow_map = {}
    data_sent_for_nanobots = {}

    for number in nanobot_numbers:

        # flow data
        provider = DataProvider('../data/data-3h-{}-nanobots.csv'.format(number))
        records = provider.nanobot_records
        blood_vessels_map = provider.get_blood_vessels_map()

        # collisions
        detector = CollisionDetector(provider.transmission_records, blood_vessels_map)
        collisions = detector.collisions

        data_sent_for_nanobots[number] = []

        for i in range(test_size):
            flow_map.clear()
            for record in records:
                simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
                if record.is_from_datasource_to_nanobot():
                    if simulator.will_transmit_from_data_source_to_nanobot():
                        packet = DataPacket()
                        packet.set(record)
                        flow_map[packet.nanobot_id] = packet
                if record.is_from_nanobot_to_access_point():
                    if record.id not in collisions:
                        if simulator.will_transmit_from_nanobot_to_access_point():
                            if record.nanobot_id in flow_map.keys():
                                packet = flow_map[record.nanobot_id]
                                packet.complete(record)
                                data_sent_for_nanobots[number].append(packet)
                                break

    xs = [number for number in data_sent_for_nanobots.keys()]
    ys = [np.mean(data_sent_for_nanobots[number]) for number in xs]

    figure, axis = plt.subplots()
    axis.set_xlabel("Number of nanobots")
    axis.set_ylabel("Average delivery time [h]")
    axis.set_title("Average delivery time as function of number of nanobots")
    axis.scatter(xs, ys)
    plt.show()

