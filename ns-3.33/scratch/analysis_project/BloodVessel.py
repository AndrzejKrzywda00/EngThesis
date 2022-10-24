class BloodVessel:
    def __init__(self, row):
        self.id = int(row[0])
        self.blood_velocity = float(row[1])
        self.length = float(row[2])
        self.radius = float(row[3])
