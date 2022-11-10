from Status import Status


# class representing single packet of data
# transmitted from data source to nanobot
# and delivered to access point
class DataPacket:

    def __init__(self):
        self.delay = 15 * 60
        self.nanobot_id = None
        self.sent_time = None
        self.status = Status.EMPTY
        self.received_time = None
        self.payload = []

    def set(self, record):
        self.nanobot_id = record.nanobot_id
        self.sent_time = record.timestamp
        self.status = Status.SENT

    def complete(self, record):
        self.received_time = record.timestamp
        self.status = Status.RECEIVED

    def flow_time(self):
        flow_time = self.received_time - self.sent_time
        return flow_time

    def delivery_time(self):
        return self.received_time - self.delay

    def __str__(self):
        return str(self.nanobot_id) + ", " + str(self.sent_time) + "," + str(self.received_time)
