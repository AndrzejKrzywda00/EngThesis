# Testing how often will collisions occur
from data_access.DataProvider import DataProvider

if __name__ == '__main__':

    wait_time = 60 * 10
    simulation_time_in_hours = 30

    # data access
    provider = DataProvider(wait_time, 'data/simulation_time/results-{}.csv'.format(simulation_time_in_hours))
    nanobots = provider.get_nanobots_map()
    vessels = provider.get_blood_vessels_map()

    # collision occurs when two nanobots' transmissions interleave
