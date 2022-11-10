import math


# Representation of single record created by blood-voyager-s
class NanobotRecord:
    def __init__(self, row, record_id):
        self.id = record_id
        self.nanobot_id = int(row[0])
        self.x = float(row[1])
        self.y = float(row[2])
        self.z = float(row[3])
        self.blood_vessel_id = int(row[4])
        self.stream_id = int(row[5])
        self.timestamp = float(row[6])
        self.direction = int(row[7])

    def __str__(self):
        return str(self.nanobot_id) + " in " + str(self.blood_vessel_id) + " at " + str(self.timestamp)

    def is_from_nanobot_to_access_point(self):
        return self.direction == 1

    def is_from_datasource_to_nanobot(self):
        return self.direction == -1

    def distance_to_nanobot(self, nanobot_record):
        return math.sqrt((self.x - nanobot_record.x) ** 2 + (self.y - nanobot_record.y) ** 2 + (self.z - nanobot_record.z) ** 2)
