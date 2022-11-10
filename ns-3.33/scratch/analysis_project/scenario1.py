import numpy as np

from model.DataPacket import DataPacket
from data_access.DataProvider import DataProvider
from model.Status import Status
from transmission.TransmissionSimulator import TransmissionSimulator

# Scenario .1
# Analysing how soon will data be delivered
# Depending on number of nanobots in the system
if __name__ == '__main__':

    # variables to calculate metrics:
    test_size = 500
    wait_time = 60 * 10
    simulation_time_in_hours = 12
    results = dict()
    times = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    data_sent_for_time = dict()

    for time in times:
        results[time] = []
        provider = DataProvider(wait_time, 'data/number_of_nanobots/results-{}.csv'.format(time))
        nanobot_map = provider.get_nanobots_map()
        blood_vessels_map = provider.get_blood_vessels_map()
        data_sent_for_time[time] = []

        for i in range(test_size):
            data_sent = []
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

            min_time = 4 * 60 * 60
            if len(data_sent) > 0:
                for data in data_sent:
                    if data.delivery_time(wait_time) <= min_time:
                        min_time = data.delivery_time(wait_time)
                data_sent_for_time[time].append(min_time)

        for key in data_sent_for_time.keys():
            data = data_sent_for_time[key]
            print(len(data) / test_size)

        results[time].append(np.mean(data_sent_for_time[time]))

    print([result[0] / 3600 for result in results.values()])
