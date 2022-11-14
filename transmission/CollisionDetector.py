from transmission.TransmissionParameters import TransmissionParameters


# Collisions only occur when nanobots are transmitting
class CollisionDetector:

    def __init__(self, records, blood_vessel_map):
        self.collisions = []
        self.vessels = blood_vessel_map
        self.data = sorted(records, key=lambda x: x.timestamp)
        self.parameters = TransmissionParameters()
        self.collisions_amount = 0
        self.collisions_all = 0

        for i in range(len(self.data)):
            record = self.data[i]
            j = i
            while j < len(self.data)-1:
                j += 1
                comparison_record = self.data[j]
                if comparison_record.timestamp - record.timestamp <= self.parameters.sampling_frequency:
                    d1 = record.distance_to(comparison_record) / 100
                    delta_t = (record.timestamp - comparison_record.timestamp)
                    d2 = delta_t * self.vessels[record.blood_vessel_id].blood_velocity
                    distance = abs(d1 + d2)
                    if distance <= 2 * self.parameters.general_transmission_distance:
                        self.collisions.append(record.id)
                        self.collisions.append(comparison_record.id)
                    break
                else:
                    break

    def will_collide(self, record):
        return self.collisions.__contains__(record.id)

    def get_collision_ratio(self):
        return self.collisions_amount / self.collisions_all
