import numpy as np

from transmission.TransmissionParameters import TransmissionParameters


# Collisions only occur when nanobots are transmitting
class CollisionDetector:

    def __init__(self, records, blood_vessel_map):
        self.collisions = []
        self.vessels = blood_vessel_map
        self.data = []
        self.parameters = TransmissionParameters()

        for record in records:
            if record.is_from_nanobot_to_access_point():
                self.data.append(record)

        for i in range(len(self.data)):
            record = self.data[i]
            # vessel = self.vessels[record.blood_vessel_id]
            j = i
            while j < len(self.data)-1:
                j += 1
                comparison_record = self.data[j]
                if comparison_record.blood_vessel_id == record.blood_vessel_id:
                    if comparison_record.timestamp - record.timestamp <= 2 * self.parameters.sampling_frequency:
                        self.collisions.append(record.id)
                        self.collisions.append(comparison_record.id)
                    break
                else:
                    break

    def will_collide(self, record):
        return self.collisions.__contains__(record.id)
