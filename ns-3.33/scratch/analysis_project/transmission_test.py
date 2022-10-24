import csv

from BloodVessel import BloodVessel
from DataPacket import DataPacket
from NanobotRecord import NanobotRecord
from Status import Status
from TransmissionSimulator import TransmissionSimulator


# Validating model of transmission for probability of success

if __name__ == '__main__':

    nanobot_records = []
    blood_vessels = []
    data_packets = []
    successful_transmissions = 0

    # reading data of nanobots moving through vessels
    with open('data/results-2.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            record = NanobotRecord(row)
            nanobot_records.append(record)

    # reading meta-data of vessels
    with open('data/vasculature-data.csv', 'r') as vessels_file:
        csv_reader = csv.reader(vessels_file)
        for row in csv_reader:
            vessel = BloodVessel(row)
            blood_vessels.append(vessel)

    # creating maps of data, for easier access
    nanobot_map = dict()
    for record in nanobot_records:
        nanobot_map[record.nanobot_id] = []

    for record in nanobot_records:
        nanobot_map[record.nanobot_id].append(record)

    blood_vessels_map = dict()
    for blood_vessel in blood_vessels:
        blood_vessels_map[blood_vessel.id] = blood_vessel

    data_sent = []

    # simulating transmission many times
    # to get statistical chances of correct transmission
    test_size = 100

    for n in range(test_size):
        for key in nanobot_map:
            records = nanobot_map[key]
            last_packet = DataPacket()
            for record in records:
                simulator = TransmissionSimulator(record, blood_vessels_map[record.blood_vessel_id])
                simulator.simulate()
                if simulator.transmission_succeeded():
                    successful_transmissions += 1
                    if record.is_from_datasource_to_nanobot():
                        last_packet.set(record)
                    if record.is_from_nanobot_to_access_point():
                        if last_packet.status == Status.SENT:
                            last_packet.complete(record)
                            data_sent.append(last_packet)

    print(successful_transmissions / len((test_size * nanobot_records)) * 100, "%")

    # for ability to detect signal at -100 dBm the chances of successful transmissions are around 2.4%
