import matplotlib.pyplot as plt

from DataPacket import DataPacket
from DataProvider import DataProvider
from Status import Status
from TransmissionSimulator import TransmissionSimulator

# Scenario .1
# Analysing how soon will data be delivered
# Depending on number of nanobots in the system
if __name__ == '__main__':

    # variables to calculate metrics:
    test_size = 1
    wait_time = 60 * 10
    simulation_time_in_hours = 12
    results = []

    for i in range(10):
        n = 100 * (i + 1)
        print('results-{}'.format(n), ' is done')
        provider = DataProvider(wait_time, 'data/number_of_nanobots/results-{}.csv'.format(n))
        nanobot_map = provider.get_nanobots_map()
        blood_vessels_map = provider.get_blood_vessels_map()

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

        min_time = simulation_time_in_hours * 60 * 60
        if len(data_sent) > 0:
            min_packet = data_sent[0]
            for data in data_sent:
                if data.delivery_time(wait_time) <= min_time:
                    min_time = data.delivery_time(wait_time)
                    min_packet = data
            results.append(min_packet.delivery_time(wait_time))

    figure, axis = plt.subplots()
    nanobots = [(i + 1) * 100 for i in range(10)]
    axis.scatter(nanobots, results)
    plt.show()
