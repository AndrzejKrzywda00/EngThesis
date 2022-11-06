import numpy as np

from TransmissionParameters import TransmissionParameters


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
            vessel = self.vessels[record.blood_vessel_id]
            j = i
            while j >= 1:
                j -= 1
                comparison_record = self.data[j]
                frame_distance = vessel.blood_velocity * self.parameters.get_transmission_time_slot()
                inter_frame_distance = self.parameters.inter_frame_gap * vessel.blood_velocity
                time_difference = record.timestamp - comparison_record.timestamp
                if time_difference * vessel.blood_velocity < vessel.length:
                    absolute_distance = record.distance_to_nanobot(comparison_record) / 10
                    time_difference_distance = vessel.blood_velocity * time_difference
                    if np.absolute(absolute_distance - time_difference_distance) <= frame_distance + inter_frame_distance:
                        self.collisions.append(record)
                        self.collisions.append(comparison_record)
                else:
                    break

            j = i
            while j < len(self.data) - 1:
                j += 1
                comparison_record = self.data[j]
                frame_distance = vessel.blood_velocity * self.parameters.get_transmission_time_slot()
                inter_frame_distance = self.parameters.inter_frame_gap * vessel.blood_velocity
                time_difference = comparison_record.timestamp - record.timestamp
                if time_difference * vessel.blood_velocity < vessel.length:
                    absolute_distance = record.distance_to_nanobot(comparison_record) / 10
                    time_difference_distance = vessel.blood_velocity * time_difference
                    if np.absolute(absolute_distance - time_difference_distance) <= frame_distance + inter_frame_distance:
                        self.collisions.append(record)
                        self.collisions.append(comparison_record)
                else:
                    break

    def will_collide(self, record):
        return self.collisions.__contains__(record.id)
