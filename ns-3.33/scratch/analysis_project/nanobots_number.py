import numpy as np

from model.DataPacket import DataPacket
from data_access.DataProvider import DataProvider
from transmission.TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    # variables to calculate metrics
    test_size = 100
    simulation_time_in_hours = 30
    nanobot_number = 100

    provider = DataProvider('data/simulation_time/results-{}.csv'.format(simulation_time_in_hours))
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()
    flow_map = {}
    data_sent = []

    s_ds_nb = 0
    ds_nb = 0
    nb_ap = 0
    s_nb_ap = 0

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
                ds_nb += 1
                if simulator.will_transmit_from_data_source_to_nanobot():
                    s_ds_nb += 1
                    packet = DataPacket()
                    packet.set(record)
                    flow_map[packet.nanobot_id] = packet
            if record.is_from_nanobot_to_access_point():
                nb_ap += 1
                if simulator.will_transmit_from_nanobot_to_access_point():
                    s_nb_ap += 1
                    if record.nanobot_id in flow_map.keys():
                        packet = flow_map[record.nanobot_id]
                        packet.complete(record)
                        data_sent.append(packet)
                        break

    print(np.mean([packet.delivery_time() for packet in data_sent]))
    print(s_ds_nb / ds_nb)
    print(s_nb_ap / nb_ap)
