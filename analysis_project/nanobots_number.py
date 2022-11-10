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
    records = provider.nanobot_records
    blood_vessels_map = provider.get_blood_vessels_map()

    flow_map = {}
    data_sent = []

    for i in range(test_size):
        print('test:', i)
        flow_map.clear()
        for record in records:
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
                        break

    print(np.mean([packet.delivery_time() for packet in data_sent]))

