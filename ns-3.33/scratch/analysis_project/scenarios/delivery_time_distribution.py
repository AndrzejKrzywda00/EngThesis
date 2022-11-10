import matplotlib.pyplot as plt
import numpy as np

from model.DataPacket import DataPacket
from data_access.DataProvider import DataProvider
from model.Status import Status
from transmission.TransmissionSimulator import TransmissionSimulator


if __name__ == '__main__':

    test_size = 1000
    simulation_time_in_hours = 8
    nanobot_number = 800

    provider = DataProvider('data/number_of_nanobots/results-{}.csv'.format(nanobot_number))
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
            if packet.delivery_time(wait_time) <= min_time:
                min_time = packet.delivery_time(wait_time)
                min_packet = packet
        if min_packet is not None:
            data_sent.append(min_packet)

    # preparing and showing results
    sampling_depth = 2
    histogram_width = 60 * 60 / sampling_depth
    widths = [[i * histogram_width, (i+1) * histogram_width] for i in range(simulation_time_in_hours * sampling_depth)]
    delivery_times = [data.delivery_time(wait_time) for data in data_sent]
    histogram = dict()

    for time in delivery_times:
        for width in widths:
            histogram[np.mean(width)] = 0

    for time in delivery_times:
        for width in widths:
            if width[0] < time <= width[1]:
                histogram[np.mean(width)] += 1

    # Probability density
    figure, axis = plt.subplots()
    values = [int(histogram[key]) for key in histogram.keys()]
    x = [key / 3600 for key in list(histogram.keys())]
    axis.bar(x, values, linewidth=1.0, edgecolor='black', width=0.5)
    axis.set_ylabel("Number of packets delivered")
    axis.set_xlabel("Delivery time [h]")
    axis.set_title("Delivery time of packets histogram, N = {} nanobots".format(nanobot_number))
    plt.show()

    print("Mean delay [h]: ", np.mean(delivery_times) / 3600)
    print("Standard deviation [h]: ", np.std(delivery_times) / 3600)
    print("Delivery percentage: ", len(data_sent) / test_size)

    # Distribution function
    distribution = []
    for width in widths:
        receptions = 0
        for data in data_sent:
            if data.received_time <= width[1]:
                receptions += 1
        distribution.append(receptions / test_size)

    dist_figure, dist_axis = plt.subplots()
    y_dist = [100 * probability for probability in distribution]
    dist_axis.stem(x, y_dist, use_line_collection=True, linefmt=':')
    dist_axis.set_title('Chances of packet delivery depending on operating time \n of N = {} nanobots in human bloodstream'.format(nanobot_number))
    dist_axis.set_ylabel('Chances of packet delivery [%]')
    dist_axis.set_xlabel('Time of operating in human body [h]')
    plt.show()
