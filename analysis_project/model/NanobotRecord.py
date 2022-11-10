import math

from model.Position3D import Position3D
from transmission.TransmissionParameters import TransmissionParameters


# Representation of single record created by blood-voyager-s
class NanobotRecord:

    def __init__(self, row, record_id):
        self.id = record_id
        self.nanobot_id = int(row[0])
        self.position = Position3D(float(row[1]), float(row[2]), float(row[3]))
        self.blood_vessel_id = int(row[4])
        self.stream_id = int(row[5])
        self.timestamp = float(row[6])
        self.parameters = TransmissionParameters()

    def __str__(self):
        return str(self.nanobot_id) + " in " + str(self.blood_vessel_id) + " at " + str(self.timestamp)

    def is_from_nanobot_to_access_point(self):
        return self.blood_vessel_id == self.parameters.ap_vessel_id

    def is_from_datasource_to_nanobot(self):
        return self.blood_vessel_id == self.parameters.ds_vessel_id

    def distance_to(self, position):
        return math.sqrt(
            (self.position.x - position.x) ** 2 +
            (self.position.y - position.y) ** 2 +
            (self.position.z - position.z) ** 2
        )
