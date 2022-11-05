from CollisionDetector import CollisionDetector
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
    simulation_time_in_hours = 30
    test_size = 100

    provider = DataProvider(wait_time, 'data/simulation_time/results-{}.csv'.format(simulation_time_in_hours))
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()

    transmissions_ds_nb = 0
    transmissions_nb_ap = 0
    successful_transmissions_ds_nb = 0
    successful_transmissions_nb_ap = 0
    num_of_nanobots = len(nanobot_map)
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
                        last_packet.complete(record)
                        data_sent.append(last_packet)

    print('Packets per hour: ', len(data_sent) / (simulation_time_in_hours * test_size))
