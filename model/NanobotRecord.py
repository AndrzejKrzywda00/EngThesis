from transmission.TransmissionParameters import TransmissionParameters


# Representation of single record created by blood-voyager-s
class NanobotRecord:

    def __init__(self, row, record_id):
        self.id = record_id
        self.nanobot_id = int(row[0])
        self.timestamp = float(row[1])
        self.blood_vessel_id = int(row[2])
        self.parameters = TransmissionParameters()

    def __str__(self):
        return str(self.nanobot_id) + " in " + str(self.blood_vessel_id) + " at " + str(self.timestamp)

    def is_from_nanobot_to_access_point(self):
        return self.blood_vessel_id == self.parameters.ap_vessel_id

    def is_from_datasource_to_nanobot(self):
        return self.blood_vessel_id == self.parameters.ds_vessel_id
