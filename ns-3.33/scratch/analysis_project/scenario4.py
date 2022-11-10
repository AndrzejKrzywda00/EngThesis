from transmission.CollisionDetector import CollisionDetector
from model.DataPacket import DataPacket
from data_access.DataProvider import DataProvider
from transmission.TransmissionSimulator import TransmissionSimulator

if __name__ == '__main__':

    wait_time = 20 * 60     # 20 minutes
    simulation_time_in_hours = 30
    test_size = 100

    provider = DataProvider('data/simulation_time/results-{}.csv'.format(simulation_time_in_hours))
    nanobots = provider.get_nanobots_map()
    vessels = provider.get_blood_vessels_map()

    transmissions_ds_nb = 0
    transmissions_nb_ap = 0
    successful_transmissions_ds_nb = 0
    successful_transmissions_nb_ap = 0
    num_of_nanobots = len(nanobots)
    data_sent = []

    for i in range(test_size):
        for nanobot_id in nanobots:
            records = nanobots[nanobot_id]
            collisions = CollisionDetector(records, vessels).collisions
            last_packet = DataPacket()
            for record in records:
                simulator = TransmissionSimulator(record, vessels[record.blood_vessel_id])
                if record.is_from_datasource_to_nanobot():
                    transmissions_ds_nb += 1
                    if simulator.will_transmit_from_data_source_to_nanobot():
                        last_packet = DataPacket()
                        last_packet.set(record)
                        successful_transmissions_ds_nb += 1
                if record.is_from_nanobot_to_access_point():
                    transmissions_nb_ap += 1
                    if not collisions.__contains__(record.id):
                        if simulator.will_transmit_from_nanobot_to_access_point():
                            last_packet.complete(record)
                            data_sent.append(last_packet)
                            successful_transmissions_nb_ap += 1

    print(successful_transmissions_nb_ap / transmissions_nb_ap)
    print(successful_transmissions_ds_nb / transmissions_ds_nb)
