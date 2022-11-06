import csv

from BloodVessel import BloodVessel
from NanobotRecord import NanobotRecord


# Provides with nanobot records data for scenarios
class DataProvider:

    def __init__(self, path):
        self.path = path
        self.delay = 15 * 60
        self.nanobot_records = []
        self.blood_vessels = []
        self.read_data()

    def read_data(self):
        with open(self.path, 'r') as file:
            csv_reader = csv.reader(file)
            record_id = 0
            for row in csv_reader:
                record = NanobotRecord(row, record_id)
                record_id += 1
                if record.timestamp >= self.delay:
                    self.nanobot_records.append(record)

        with open('data/vasculature-data.csv', 'r') as vessels_file:
            csv_reader = csv.reader(vessels_file)
            for row in csv_reader:
                vessel = BloodVessel(row)
                self.blood_vessels.append(vessel)

    def get_nanobots_map(self):
        nanobot_map = dict()
        for record in self.nanobot_records:
            nanobot_map[record.nanobot_id] = []

        for record in self.nanobot_records:
            nanobot_map[record.nanobot_id].append(record)
        return nanobot_map

    def get_blood_vessels_map(self):
        blood_vessels_map = dict()
        for blood_vessel in self.blood_vessels:
            blood_vessels_map[blood_vessel.id] = blood_vessel
        return blood_vessels_map
