from DataPacket import DataPacket
from DataProvider import DataProvider

# Simulation to check how many packets per unit of time
# will be delivered by the system
# 100 nanobots | 30 h
# System working in steady time, not stopping after receiving first packet
from TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    # variables to calculate metrics
    wait_time = 10 * 60
    simulation_time_in_hours = 7
    test_size = 10
    nanobots_number = 1000

    provider = DataProvider('data/number_of_nanobots/results-{}.csv'.format(nanobots_number))
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()

    num_of_nanobots = len(nanobot_map)
    data_sent = []
    flow_map = {}

    all_records = []
    for nanobot_id in nanobot_map:
        records = nanobot_map[nanobot_id]
        for record in records:
            all_records.append(record)

    all_records.sort(key=lambda x: x.timestamp)

    for i in range(test_size):
        print('test:', i)
        flow_map.clear()
        for record in all_records:
            simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
            if record.is_from_datasource_to_nanobot():
                if simulator.will_transmit_from_data_source_to_nanobot():
                    packet = DataPacket()
                    packet.set(record)
                    flow_map[packet.nanobot_id] = packet
            if record.is_from_nanobot_to_access_point():
                if simulator.will_transmit_from_nanobot_to_access_point():
                    if record.nanobot_id in flow_map.keys():
                        packet = flow_map[record.nanobot_id]
                        packet.complete(record)
                        data_sent.append(packet)

    print('Packets per hour: ', len(data_sent) / (simulation_time_in_hours * test_size * 3600))
