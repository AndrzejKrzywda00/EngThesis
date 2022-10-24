# Simulating transmission
# from nanobot to access point scenario
# OR
# from data source to nanobot(s)
# 1
# ------------------------------------------
# (n) ->
# -----------------(AP)---------------------

import math
import random as random

from TransmissionParameters import TransmissionParameters


def spread_loss(f, d):
    return (4 * math.pi * f * d / 3e8) ** 2


def absorption_loss(d):
    kf_blood = 2.15e4
    scale = min(kf_blood * d, 50)
    return math.exp(scale)


class TransmissionSimulator:

    def __init__(self, nanobot_record, vessel):
        self.vessel = vessel
        self.nanobot_record = nanobot_record
        self.positions = []
        self.reception_level = -130  # dBm
        self.power = 0
        self.parameters = TransmissionParameters()

    def will_transmit_from_data_source_to_nanobot(self):
        self.prepare_data()
        distance = self.parameters.get_transmission_time_slot() * self.parameters.reception_to_transmission_ratio * self.vessel.blood_velocity
        macro_slots = [[position, [position[0], position[1], position[2] + distance]] for position in self.positions]

        time_offset = random.random() * (self.parameters.inter_frame_gap + self.parameters.get_transmission_time_slot())
        distance_offset = time_offset * self.vessel.blood_velocity

        for slot in macro_slots:
            start_position = slot[0]
            start_position[2] += distance_offset
            end_position = slot[1]
            current_position = start_position
            time_slot_distance = self.parameters.get_transmission_time_slot() * self.vessel.blood_velocity
            while current_position[2] + time_slot_distance < end_position[2]:
                active_slot = [current_position,
                               [current_position[0],
                                current_position[1],
                                current_position[2] + time_slot_distance]]
                if self.is_in_range(active_slot[0]) and self.is_in_range(active_slot[1]):
                    return True
                else:
                    current_position[2] += time_slot_distance + self.parameters.inter_frame_gap * self.vessel.blood_velocity
        return False

    def will_transmit_from_nanobot_to_access_point(self):
        self.prepare_data()
        distance = self.parameters.get_transmission_time_slot() * self.vessel.blood_velocity
        slots = [[position, [position[0], position[1], position[2] + distance]] for position in self.positions]

        for slot in slots:
            if self.is_in_range(slot[0]) and self.is_in_range(slot[1]):
                return True
        return False

    def is_in_range(self, position):
        frequency = self.parameters.central_frequency
        distance = math.sqrt(position[0] ** 2 + position[1] ** 2 + position[2] ** 2)
        total_loss = 10 * math.log10(spread_loss(frequency, distance)) + 10 * math.log10(absorption_loss(distance))
        if self.power - total_loss >= self.reception_level:
            return True
        return False

    def prepare_data(self):
        n = 0
        simulation_time = self.vessel.length / self.vessel.blood_velocity
        offset = random.random()
        time_steps = []

        while offset + n < simulation_time:
            time_steps.append(offset + n)
            n += 1

        nanobot_angle = random.random() * 360
        nanobot_diameter = random.random() * 0.006
        nanobot_radius = nanobot_diameter / 2
        nanobot_x = nanobot_radius * math.cos(nanobot_angle / (2 * math.pi))
        nanobot_y = nanobot_radius * math.sin(nanobot_angle / (2 * math.pi))
        nanobot_z = -self.vessel.length / 2

        for time_step in time_steps:
            position = [nanobot_x, nanobot_y, nanobot_z + time_step * self.vessel.blood_velocity]
            self.positions.append(position)
