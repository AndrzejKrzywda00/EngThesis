# Data holder class for transmission parameters to construct concrete transmission scenarios

class TransmissionParameters:
    def __init__(self):
        self.frame_length = 64 * 8  # 512 bits
        self.transmission_speed = 1e6  # 1 Mb/s

        # ratio of time the nanobot can listen / transmit with the same amount of energy
        self.reception_to_transmission_ratio = 10

        self.inter_frame_gap = 1e-5     # 10 us
        self.central_frequency = 1e12   # 1 THz

        self.sampling_frequency = 2     # info every 2 seconds
        self.ds_vessel_id = 25
        self.ap_vessel_id = 64

        self.general_transmission_distance = 0.001

    def get_transmission_slot_time(self):
        return self.frame_length / self.transmission_speed
