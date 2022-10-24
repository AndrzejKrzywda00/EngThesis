import matplotlib.pyplot as plt

from DataPacket import DataPacket
from DataProvider import DataProvider
from Status import Status
from TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    # variables to define scenario
    wait_time = 10 * 60
    simulation_hours = [(i+1) * 2 for i in range(15)]
    test_size = 100
    results = dict()

    # defining the scenario
    for hour in simulation_hours:
        print("for hour {}".format(hour))
        provider = DataProvider(wait_time, 'data/simulation_time/results-{}.csv'.format(hour))
        nanobot_map = provider.get_nanobots_map()
        blood_vessels_map = provider.get_blood_vessels_map()
        data_sent = []

        for i in range(test_size):
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
                                data_sent.append(last_packet)
                                break
                else:
                    continue
                break
        results[hour] = len(data_sent) / test_size

    # after simulating scenario, we show data
    figure, axis = plt.subplots()
    ys = [results[hour]*100 for hour in simulation_hours]
    axis.stem(simulation_hours, ys, linefmt='b:', use_line_collection=True)
    axis.set_ylabel('Chances of packet delivery [%]')
    axis.set_xlabel('Time of system operating in human body [h]')
    plt.show()
