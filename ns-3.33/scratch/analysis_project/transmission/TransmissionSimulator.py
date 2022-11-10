import math
import random as random

import numpy as np

from model.Position3D import Position3D
from TransmissionParameters import TransmissionParameters


def spread_loss(f, d):
    return (4 * math.pi * f * d / 3e8) ** 2


def absorption_loss(d):
    kf_blood = 2.15e4
    scale = min(kf_blood * d, 50)
    return math.exp(scale)


# Simulating transmission
# from nanobot to access point scenario
# and
# from data source to nanobot
class TransmissionSimulator:

    def __init__(self, nanobot_record, vessel):
        self.access_point = Position3D(0, 0, 0)
        self.power_load_time = 1
        self.vessel = vessel
        self.nanobot_record = nanobot_record
        self.positions = []
        self.reception_level = -130  # dBm
        self.power = 0
        self.parameters = TransmissionParameters()

    def will_transmit_from_data_source_to_nanobot(self):
        self.prepare_data()
        distance = self.parameters.get_transmission_slot_time() * self.parameters.reception_to_transmission_ratio * self.vessel.blood_velocity
        macro_slots = []
        for position in self.positions:
            macro_slots.append([position, Position3D(position.x, position.y, position.z + distance)])

        time_offset = random.random() * (self.parameters.inter_frame_gap + self.parameters.get_transmission_slot_time())
        distance_offset = time_offset * self.vessel.blood_velocity

        for slot in macro_slots:
            start_position = slot[0]
            start_position.set_z(start_position.z + distance_offset)
            end_position = slot[1]
            current_position = start_position
            time_slot_distance = self.parameters.get_transmission_slot_time() * self.vessel.blood_velocity
            while current_position.z + time_slot_distance < end_position.z:
                next_position = Position3D(current_position.x, current_position.y, current_position.z + time_slot_distance)
                active_slot = [current_position, next_position]
                if self.is_in_range(active_slot[0]) and self.is_in_range(active_slot[1]):
                    return True
                else:
                    current_position.set_z(current_position.z + time_slot_distance + self.parameters.inter_frame_gap * self.vessel.blood_velocity)
        return False

    def will_transmit_from_nanobot_to_access_point(self):
        self.prepare_data()
        distance = self.parameters.get_transmission_slot_time() * self.vessel.blood_velocity
        slots = []
        for position in self.positions:
            slots.append([position, Position3D(position.x, position.y, position.z + distance)])

        for slot in slots:
            if self.is_in_range(slot[0]) and self.is_in_range(slot[1]):
                return True
        return False

    def is_in_range(self, position):
        frequency = self.parameters.central_frequency
        distance = position.distance_to(self.access_point)
        total_loss = 10 * math.log10(spread_loss(frequency, distance)) + 10 * math.log10(absorption_loss(distance))
        if self.power - total_loss >= self.reception_level:
            return True
        return False

    def prepare_data(self):
        n = 0
        simulation_time = self.vessel.length / self.vessel.blood_velocity
        time_offset = random.random() * self.power_load_time
        time_steps = []

        while time_offset + n < simulation_time:
            time_steps.append(time_offset + n)
            n += self.power_load_time

        angles = np.random.uniform(0.0, 2.0 * np.pi, 1)
        radius = self.vessel.radius * np.sqrt(np.random.uniform(0.0, 1.0, 1))

        nanobot_x = radius[0] * np.cos(angles[0]) + self.vessel.radius
        nanobot_y = radius[0] * np.sin(angles[0])
        nanobot_z = -self.vessel.length / 2

        for time_step in time_steps:
            position = Position3D(nanobot_x, nanobot_y, nanobot_z + self.vessel.blood_velocity * time_step)
            self.positions.append(position)
