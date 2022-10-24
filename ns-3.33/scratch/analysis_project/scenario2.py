import matplotlib.pyplot as plt
import numpy as np

from DataPacket import DataPacket
from DataProvider import DataProvider
from Status import Status
from TransmissionSimulator import TransmissionSimulator

# Scenario .2
# Analysing how soon first packet of data will be delivered
# On 1000 examples
# And plotting a histogram
if __name__ == '__main__':

    # variables to calculate metrics
    test_size = 1000
    distribution_threshold = 10 * 60
    simulation_time_in_hours = 30

    provider = DataProvider(distribution_threshold, 'data/results-30.csv')
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()

    data_sent = []
    data_sent_for_test = dict()

    for i in range(test_size):
        data_sent_for_test[i] = []
        for nanobot_id in nanobot_map:
            records = nanobot_map[nanobot_id]
            last_packet = DataPacket()
            for record in records:
                simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
                if record.is_from_datasource_to_nanobot():
                    if simulator.will_transmit_from_data_source_to_nanobot():
                        last_packet = DataPacket()
                        last_packet.set(record)
                if record.is_from_nanobot_to_access_point():
                    if simulator.will_transmit_from_nanobot_to_access_point():
                        if last_packet.status == Status.SENT:
                            last_packet.complete(record)
                            data_sent_for_test[i].append(last_packet)

    # finding first packet delivered for each nanobot
    for key in data_sent_for_test.keys():
        packets = data_sent_for_test[key]
        min_time = simulation_time_in_hours * 60 * 60
        min_packet = None
        for packet in packets:
            if packet.delivery_time(distribution_threshold) <= min_time:
                min_time = packet.delivery_time(distribution_threshold)
                min_packet = packet
        if min_packet is not None:
            data_sent.append(min_packet)

    # preparing and showing results
    sampling_depth = 2
    histogram_width = 60 * 60 / sampling_depth
    widths = [[i * histogram_width, (i+1) * histogram_width] for i in range(simulation_time_in_hours * sampling_depth)]
    delivery_times = [data.delivery_time(distribution_threshold) for data in data_sent]
    histogram = dict()

    for time in delivery_times:
        for width in widths:
            histogram[np.mean(width)] = 0

    for time in delivery_times:
        for width in widths:
            if width[0] < time <= width[1]:
                histogram[np.mean(width)] += 1

    figure, axis = plt.subplots()
    values = [int(histogram[key]) for key in histogram.keys()]
    x = [key / 3600 for key in list(histogram.keys())]
    axis.bar(x, values, linewidth=1.0, edgecolor='black', width=0.5)
    axis.set_ylabel("Number of packets delivered")
    axis.set_xlabel("Delivery time [h]")
    axis.set_title("Delivery time of packets histogram")
    plt.show()

    print("mean delay [h]: ", np.mean(delivery_times) / 3600)
    print("standard deviation [h]: ", np.std(delivery_times) / 3600)
    print("Delivery percentage: ", len(data_sent) / test_size)
