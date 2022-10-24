class NanobotRecord:
    def __init__(self, row):
        self.nanobot_id = int(row[0])
        self.x = float(row[1])
        self.y = float(row[2])
        self.z = float(row[3])
        self.blood_vessel_id = int(row[4])
        self.stream_id = int(row[5])
        self.timestamp = float(row[6])
        self.direction = int(row[7])

    def __str__(self):
        return str(self.nanobot_id) + ", " + str(self.blood_vessel_id) + ", " + str(self.timestamp)

    def is_from_nanobot_to_access_point(self):
        return self.direction == -1

    def is_from_datasource_to_nanobot(self):
        return self.direction == 1
