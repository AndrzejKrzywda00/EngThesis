from DataPacket import DataPacket
from DataProvider import DataProvider
from TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    # variables to calculate metrics
    test_size = 1
    wait_time = 10 * 60
    simulation_time_in_hours = 30
    nanobot_number = 200

    provider = DataProvider(wait_time, 'data/number_of_nanobots/results-{}.csv'.format(nanobot_number))
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()
    flow_map = {}
    data_sent = []
    transmissions = 0
    successful_transmissions = 0

    all_records = []
    for nanobot_id in nanobot_map:
        records = nanobot_map[nanobot_id]
        for record in records:
            all_records.append(record)

    all_records.sort(key=lambda x: x.timestamp)

    for i in range(test_size):
        flow_map.clear()
        for record in all_records:
            simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
            if record.is_from_datasource_to_nanobot():
                if simulator.will_transmit_from_data_source_to_nanobot():
                    packet = DataPacket()
                    packet.set(record)
                    flow_map[packet.nanobot_id] = packet
            if record.is_from_nanobot_to_access_point():
                transmissions += 1
                if simulator.will_transmit_from_nanobot_to_access_point():
                    print(record)
                    if record.nanobot_id in flow_map.keys():
                        successful_transmissions += 1
                        packet = flow_map[record.nanobot_id]
                        packet.complete(record)
                        data_sent.append(packet)
                        break

    # print(np.mean([packet.delivery_time(wait_time) / 3600 for packet in data_sent]))
    print(len(data_sent))
    print(transmissions)
