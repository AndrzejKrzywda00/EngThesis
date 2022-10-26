from DataPacket import DataPacket
from DataProvider import DataProvider

# Simulating to check how often do transmissions occur
# per time unit in two scenarios
# DS -> NB
# NB -> AP
from Status import Status
from TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    # variables to calculate metrics
    test_size = 1000
    wait_time = 10 * 60
    simulation_time_in_hours = 30

    provider = DataProvider(wait_time, 'data/simulation_time/results-{}.csv'.format(simulation_time_in_hours))
    nanobot_map = provider.get_nanobots_map()
    blood_vessels_map = provider.get_blood_vessels_map()

    transmissions_ds_nb = 0
    transmissions_nb_ap = 0
    successful_transmissions_ds_nb = 0
    successful_transmissions_nb_ap = 0

    for i in range(test_size):
        for nanobot_id in nanobot_map:
            records = nanobot_map[nanobot_id]
            last_packet = DataPacket()
            for record in records:
                simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
                if record.is_from_datasource_to_nanobot():
                    transmissions_ds_nb += 1
                    if simulator.will_transmit_from_data_source_to_nanobot():
                        successful_transmissions_ds_nb += 1
                if record.is_from_nanobot_to_access_point():
                    transmissions_nb_ap += 1
                    if simulator.will_transmit_from_nanobot_to_access_point():
                        successful_transmissions_nb_ap += 1

    print(successful_transmissions_ds_nb / transmissions_ds_nb)
    print(successful_transmissions_nb_ap / transmissions_nb_ap)
    print(transmissions_ds_nb / (simulation_time_in_hours * test_size))
    print(transmissions_nb_ap / (simulation_time_in_hours * test_size))
