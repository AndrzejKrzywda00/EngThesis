from transmission.TransmissionParameters import TransmissionParameters
from transmission.TransmissionSimulator import TransmissionSimulator


# Collisions only occur when nanobots are transmitting
class CollisionDetector:

    def __init__(self, records, blood_vessel_map):
        self.collisions = []
        self.vessels = blood_vessel_map
        self.data = records
        self.parameters = TransmissionParameters()

        for i in range(len(self.data)):
            record = self.data[i]
            j = i
            while j < len(self.data) - 1:
                j += 1
                comparison_record = self.data[j]
                if comparison_record.timestamp - record.timestamp <= self.parameters.sampling_frequency:
                    record_simulator = TransmissionSimulator(record, self.vessels[record.blood_vessel_id])
                    comparison_record_simulator = TransmissionSimulator(comparison_record, self.vessels[comparison_record.blood_vessel_id])
                    if record_simulator.will_transmit_from_nanobot_to_access_point():
                        if comparison_record_simulator.will_transmit_from_nanobot_to_access_point():
                            self.collisions.append(record.id)
                            self.collisions.append(comparison_record.id)
                else:
                    break
